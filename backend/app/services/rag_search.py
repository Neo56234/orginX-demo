"""
RAG search service: BM25 (PostgreSQL tsvector) + Vector (pgvector) + RRF fusion.
Used by the /chat endpoint to find relevant known_cases before LLM generation.
"""
import logging
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import text

logger = logging.getLogger("originx.services.rag_search")

_embedding_model = None

def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
        logger.info("Loaded multilingual embedding model")
    return _embedding_model


def embed_text(text: str) -> list[float]:
    model = _get_embedding_model()
    return model.encode(text, normalize_embeddings=True).tolist()


def bm25_search(db: Session, query: str, limit: int = 10) -> list[dict]:
    """Full-text BM25 search using PostgreSQL tsvector with OR matching."""
    # Build OR query: "mob july 2024" → "mob | july | 2024"
    words = [w for w in query.replace("'", "").split() if len(w) > 1]
    or_query = " | ".join(words) if words else query

    sql = text("""
        SELECT
            id,
            title_en,
            title_bn,
            false_claim_en,
            false_claim_bn,
            actual_origin_country,
            actual_origin_city,
            actual_origin_date,
            debunk_url,
            debunk_source,
            keywords,
            ts_rank(search_vector, to_tsquery('simple', :or_query)) AS rank
        FROM known_cases
        WHERE search_vector @@ to_tsquery('simple', :or_query)
           OR keywords::text ILIKE :keyword_like
        ORDER BY rank DESC
        LIMIT :limit
    """)
    rows = db.execute(sql, {
        "or_query": or_query,
        "keyword_like": f"%{query.lower()[:40]}%",
        "limit": limit,
    }).fetchall()
    return [dict(r._mapping) for r in rows]


def vector_search(db: Session, query: str, limit: int = 10) -> list[dict]:
    """Semantic vector search using pgvector cosine similarity."""
    embedding = embed_text(query)
    sql = text("""
        SELECT
            id,
            title_en,
            title_bn,
            false_claim_en,
            false_claim_bn,
            actual_origin_country,
            actual_origin_city,
            actual_origin_date,
            debunk_url,
            debunk_source,
            keywords,
            1 - (text_embedding <=> :embedding::vector) AS similarity
        FROM known_cases
        WHERE text_embedding IS NOT NULL
        ORDER BY text_embedding <=> :embedding::vector
        LIMIT :limit
    """)
    rows = db.execute(sql, {
        "embedding": str(embedding),
        "limit": limit,
    }).fetchall()
    return [dict(r._mapping) for r in rows]


def rrf_fusion(bm25_results: list[dict], vector_results: list[dict], k: int = 60) -> list[dict]:
    """
    Reciprocal Rank Fusion: score = 1/(k + rank_bm25) + 1/(k + rank_vector)
    Returns merged list sorted by RRF score descending.
    """
    scores: dict[int, float] = {}
    meta: dict[int, dict] = {}

    for rank, row in enumerate(bm25_results):
        rid = row["id"]
        scores[rid] = scores.get(rid, 0.0) + 1.0 / (k + rank + 1)
        meta[rid] = row

    for rank, row in enumerate(vector_results):
        rid = row["id"]
        scores[rid] = scores.get(rid, 0.0) + 1.0 / (k + rank + 1)
        meta[rid] = row

    sorted_ids = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)
    results = []
    for rid in sorted_ids:
        row = dict(meta[rid])
        row["rrf_score"] = scores[rid]
        results.append(row)
    return results


def search_incidents(db: Session, query: str, top_k: int = 5) -> list[dict]:
    """
    Main entry point: BM25 + Vector search → RRF fusion → top_k results.
    Falls back to keyword-only if no embeddings exist yet.
    """
    bm25 = bm25_search(db, query, limit=10)
    try:
        vector = vector_search(db, query, limit=10)
    except Exception as e:
        logger.warning("Vector search failed (embeddings may not be seeded yet): %s", e)
        vector = []

    if not bm25 and not vector:
        return []

    fused = rrf_fusion(bm25, vector)
    return fused[:top_k]


def format_context(results: list[dict]) -> str:
    """Format search results as context string for LLM prompt."""
    if not results:
        return "No matching incidents found in the database."

    lines = []
    for i, r in enumerate(results, 1):
        date = str(r.get("actual_origin_date") or "Unknown date")
        city = r.get("actual_origin_city") or ""
        country = r.get("actual_origin_country") or "Unknown"
        location = f"{city}, {country}" if city else country
        source = r.get("debunk_url") or r.get("debunk_source") or "OriginX DB"

        lines.append(
            f"[{i}] {r.get('title_en', 'Untitled')}\n"
            f"    False claim: {r.get('false_claim_en', 'N/A')}\n"
            f"    Actual origin: {location} | Date: {date}\n"
            f"    Source: {source}"
        )
    return "\n\n".join(lines)
