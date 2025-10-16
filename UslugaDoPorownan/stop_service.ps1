# PowerShell script to stop Document Comparison Service

Write-Host "[INFO] Zatrzymywanie uslugi..." -ForegroundColor Cyan

# Znajdz procesy Python z uvicorn
$processes = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue |
    Select-Object -ExpandProperty OwningProcess -Unique

if ($processes) {
    foreach ($pid in $processes) {
        Write-Host "[INFO] Znaleziono proces: $pid" -ForegroundColor Yellow
        try {
            Stop-Process -Id $pid -Force -ErrorAction Stop
            Write-Host "[OK] Proces $pid zatrzymany" -ForegroundColor Green
        } catch {
            Write-Host "[ERROR] Nie udalo sie zatrzymac procesu $pid" -ForegroundColor Red
        }
    }

    # Sprawdz czy faktycznie zatrzymano
    Start-Sleep -Seconds 2
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 2 -ErrorAction Stop
        Write-Host "[WARNING] Usluga nadal odpowiada!" -ForegroundColor Yellow
        exit 1
    } catch {
        Write-Host "[OK] Usluga zatrzymana pomyslnie" -ForegroundColor Green
        exit 0
    }
} else {
    Write-Host "[INFO] Usluga nie byla uruchomiona" -ForegroundColor Gray
    exit 0
}
