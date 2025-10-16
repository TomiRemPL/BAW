# PowerShell script to check Document Comparison Service status

try {
    $response = Invoke-RestMethod -Uri "http://localhost:8001/health" -TimeoutSec 2 -ErrorAction Stop

    Write-Host "[OK] Usluga dziala" -ForegroundColor Green
    Write-Host ($response | ConvertTo-Json -Depth 10)

    exit 0
} catch {
    Write-Host "[ERROR] Usluga nie dziala" -ForegroundColor Red
    Write-Host '{"status":"stopped","error":"Service not responding"}'

    exit 1
}
