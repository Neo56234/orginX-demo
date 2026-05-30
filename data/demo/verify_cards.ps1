# OriginX Phase 4 — Step 3: Verify Counter-Cards Generated
# Run after run_pipeline.ps1 completes
# Checks that every demo investigation has a counter-card PNG

$RESULTS_FILE = Join-Path $PSScriptRoot "pipeline_results.json"

if (-not (Test-Path $RESULTS_FILE)) {
    Write-Host "ERROR: pipeline_results.json not found. Run run_pipeline.ps1 first." -ForegroundColor Red
    exit 1
}

$results = Get-Content $RESULTS_FILE | ConvertFrom-Json

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  OriginX — Counter-Card Verification " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

foreach ($r in $results) {
    if (-not $r.investigation_id) { continue }

    # Check if card exists in Docker volume
    $cardCheck = docker compose -f "$PSScriptRoot\..\..\docker-compose.yml" exec api sh -c "test -f /data/cards/$($r.investigation_id).png && echo EXISTS || echo MISSING" 2>&1

    $color = if ($cardCheck -match "EXISTS") { "Green" } else { "Red" }
    $icon  = if ($cardCheck -match "EXISTS") { "[OK]" } else { "[MISSING]" }
    Write-Host "  $icon Video $($r.id): $($r.title)" -ForegroundColor $color
    Write-Host "       /data/cards/$($r.investigation_id).png" -ForegroundColor DarkGray
}

Write-Host ""
Write-Host "  If any cards are MISSING:" -ForegroundColor Yellow
Write-Host '  docker compose exec api python -c "from app.services.card_generator import generate_card; generate_card('"'"'INVESTIGATION_ID'"'"')"' -ForegroundColor Gray
Write-Host ""
