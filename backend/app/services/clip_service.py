import logging
from typing import Optional
from transformers import CLIPModel, CLIPProcessor
from PIL import Image
import torch

logger = logging.getLogger("originx.services.clip")

GEO_LABELS = [
    "a street scene in Bangladesh with CNGs and Bengali signage",
    "a street scene in Pakistan with Urdu signage and Pakistani vehicles",
    "a street scene in India with Hindi signage and Indian vehicles",
    "a Pakistani television news broadcast with Urdu text on screen",
    "an Indian television news broadcast with Hindi text on screen",
    "a large crowd protest in Lahore or Karachi Pakistan",
    "a large crowd protest in Dhaka Bangladesh",
    "Pakistani or Lahore urban architecture and buildings",
    "Indian urban architecture and buildings",
    "Bangladeshi or Dhaka urban architecture and buildings",
    "a flood or disaster rescue scene",
    "a military or police operation",
]

_model = None
_processor = None

def get_model_and_processor():
    global _model, _processor
    if _model is None or _processor is None:
        logger.info("Loading CLIP model (this may take a while)...")
        _model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        _processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return _model, _processor

def get_clip_embedding(image_path: str) -> Optional[list[float]]:
    """
    Generate CLIP ViT-B/32 embedding for an image.
    Returns list of 512 floats, or None on failure.
    """
    try:
        model, processor = get_model_and_processor()
        image = Image.open(image_path).convert("RGB")
        inputs = processor(text=[""], images=image, return_tensors="pt")
        with torch.no_grad():
            outputs = model(**inputs)
            features = outputs.image_embeds
            features = features / features.norm(dim=-1, keepdim=True)
        return features[0].tolist()
    except Exception as e:
        logger.error("Error extracting CLIP embedding for %s: %s", image_path, e)
        return None

def classify_geo(image_path: str) -> dict:
    """
    Zero-shot geographic classification using CLIP text-image similarity.
    Returns { label: str, confidence: float, all_scores: {label: score} }
    """
    try:
        model, processor = get_model_and_processor()
        image = Image.open(image_path).convert("RGB")
        inputs = processor(text=GEO_LABELS, images=image, return_tensors="pt", padding=True)
        with torch.no_grad():
            outputs = model(**inputs)
            logits_per_image = outputs.logits_per_image # this is the image-text similarity score
            probs = logits_per_image.softmax(dim=1)[0] # get probabilities
            
        all_scores = {GEO_LABELS[i]: float(probs[i]) for i in range(len(GEO_LABELS))}
        best_idx = probs.argmax().item()
        best_label = GEO_LABELS[best_idx]
        confidence = float(probs[best_idx])
        
        return {"label": best_label, "confidence": confidence, "all_scores": all_scores}
    except Exception as e:
        logger.error("Error classifying geo for %s: %s", image_path, e)
        return {"label": None, "confidence": 0.0, "all_scores": {}}
