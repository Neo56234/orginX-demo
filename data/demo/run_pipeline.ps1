# OriginX Phase 4 — Pipeline Cache Script (Windows PowerShell)
# Runs the investigation pipeline on all demo videos and caches results in DB
# Run this BEFORE demo day. Takes ~15-20 minutes total.
#
# Prerequisites:
#   1. docker compose up --build  (in the originx/ directory)
#   2. All .env keys set (ANTHROPIC_API_KEY, YOUTUBE_API_KEY, GROQ_API_KEY)

$API_BASE = "http://localhost:8000"
$DEMO_JSON = Join-Path $PSScriptRoot "demo_videos.json"
$RESULTS_FILE = Join-Path $PSScriptRoot "pipeline_results.json"

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  OriginX Phase 4 — Pipeline Cacher   " -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Health check
Write-Host "[1/4] Checking backend health..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "$API_BASE/health" -Method GET -TimeoutSec 5
    Write-Host "  Backend is UP: $($health.status)" -ForegroundColor Green
} catch {
    Write-Host "  ERROR: Backend not reachable at $API_BASE" -ForegroundColor Red
    Write-Host "  Run: cd originx && docker compose up --build" -ForegroundColor Red
    exit 1
}

# Step 2: Load demo videos
Write-Host "[2/4] Loading demo_videos.json..." -ForegroundColor Yellow
$demoData = Get-Content $DEMO_JSON | ConvertFrom-Json
$videos = $demoData.videos | Where-Object { $_.video_url -ne $null }
Write-Host "  Found $($videos.Count) videos with URLs (skipping $($demoData.videos.Count - $videos.Count) without URLs)" -ForegroundColor Green

# Step 3: Run pipeline on each video
Write-Host "[3/4] Running pipeline on each video..." -ForegroundColor Yellow
Write-Host ""

$results = @()

foreach ($v in $videos) {
    Write-Host "  Video $($v.id): $($v.title)" -ForegroundColor White
    Write-Host "  URL: $($v.video_url)" -ForegroundColor Gray

    $body = @{
        video_url       = $v.video_url
        claimed_context = $v.claimed_context
    } | ConvertTo-Json

    try {
        $response = Invoke-RestMethod -Uri "$API_BASE/api/analyze" `
            -Method POST `
            -ContentType "application/json" `
            -Body $body `
            -TimeoutSec 30

        $investigationId = $response.investigation_id
        Write-Host "  Queued: investigation_id = $investigationId" -ForegroundColor Cyan
        Write-Host "  Waiting for pipeline to complete (up to 120s)..." -ForegroundColor Gray

        # Poll for completion
        $maxWait = 120
        $waited = 0
        $completed = $false

        while ($waited -lt $maxWait) {
            Start-Sleep -Seconds 5
            $waited += 5

            try {
                $inv = Invoke-RestMethod -Uri "$API_BASE/api/investigation/$investigationId" -Method GET -TimeoutSec 10
                if ($inv.status -eq "complete" -or $inv.status -eq "failed") {
                    $completed = $true
                    break
                }
                Write-Host "  Status: $($inv.status) ($waited s)" -ForegroundColor DarkGray
            } catch {
                # continue polling
            }
        }

        if ($completed) {
            $finalInv = Invoke-RestMethod -Uri "$API_BASE/api/investigation/$investigationId" -Method GET -TimeoutSec 10
            $status = if ($finalInv.verdict -eq $v.expected_verdict) { "PASS" } else { "MISMATCH" }
            $color = if ($status -eq "PASS") { "Green" } else { "Yellow" }

            Write-Host "  Verdict: $($finalInv.verdict) (expected: $($v.expected_verdict)) [$status]" -ForegroundColor $color
            Write-Host "  Confidence: $($finalInv.confidence)%" -ForegroundColor Gray

            $results += @{
                id              = $v.id
                title           = $v.title
                video_url       = $v.video_url
                investigation_id = $investigationId
                verdict         = $finalInv.verdict
                expected_verdict = $v.expected_verdict
                confidence      = $finalInv.confidence
                status          = $status
                share_url       = "$API_BASE/share/$investigationId"
            }
        } else {
            Write-Host "  TIMEOUT: Pipeline did not complete in ${maxWait}s" -ForegroundColor Red
            $results += @{
                id              = $v.id
                title           = $v.title
                video_url       = $v.video_url
                investigation_id = $investigationId
                verdict         = "timeout"
                status          = "TIMEOUT"
            }
        }
    } catch {
        Write-Host "  ERROR: $($_.Exception.Message)" -ForegroundColor Red
        $results += @{
            id    = $v.id
            title = $v.title
            status = "ERROR"
            error  = $_.Exception.Message
        }
    }

    Write-Host ""
}

# Step 4: Save results and summary
Write-Host "[4/4] Saving results..." -ForegroundColor Yellow
$results | ConvertTo-Json -Depth 5 | Out-File -FilePath $RESULTS_FILE -Encoding utf8
Write-Host "  Results saved to: $RESULTS_FILE" -ForegroundColor Green

Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan

$passed = ($results | Where-Object { $_.status -eq "PASS" }).Count
$total = $results.Count

foreach ($r in $results) {
    $color = if ($r.status -eq "PASS") { "Green" } elseif ($r.status -eq "MISMATCH") { "Yellow" } else { "Red" }
    Write-Host "  [$($r.status)] Video $($r.id): $($r.title)" -ForegroundColor $color
    if ($r.investigation_id) {
        Write-Host "         Share: http://localhost:3000/share/$($r.investigation_id)" -ForegroundColor DarkGray
    }
}

Write-Host ""
Write-Host "  PASSED: $passed / $total" -ForegroundColor $(if ($passed -eq $total) { "Green" } else { "Yellow" })
Write-Host ""

if ($passed -lt $total) {
    Write-Host "  ACTION REQUIRED: Re-run failed videos individually before demo day." -ForegroundColor Yellow
    Write-Host "  For each failed video:" -ForegroundColor Yellow
    Write-Host '    Invoke-RestMethod -Uri "$API_BASE/api/analyze" -Method POST -ContentType "application/json" -Body '"'"'{"video_url":"URL"}'"'" -ForegroundColor Gray
}

Write-Host ""
Write-Host "  NEXT STEPS:" -ForegroundColor Cyan
Write-Host "  1. Open each investigation in browser to pre-load Mapbox tiles" -ForegroundColor White
foreach ($r in ($results | Where-Object { $_.investigation_id })) {
    Write-Host "     http://localhost:3000/investigation/$($r.investigation_id)" -ForegroundColor DarkGray
}
Write-Host "  2. Check counter-cards exist:" -ForegroundColor White
Write-Host "     docker compose exec api ls /data/cards/" -ForegroundColor DarkGray
Write-Host "  3. Run verify_cards.ps1 to confirm all PNGs are generated" -ForegroundColor White
