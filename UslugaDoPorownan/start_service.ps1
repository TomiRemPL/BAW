# PowerShell script to start Document Comparison Service

Write-Host "[INFO] Sprawdzanie czy usluga juz dziala..." -ForegroundColor Cyan

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 2 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] Usluga juz dziala na porcie 8001" -ForegroundColor Green
        exit 0
    }
} catch {
    Write-Host "[INFO] Usluga nie dziala, uruchamianie..." -ForegroundColor Yellow
}

# Zmien katalog na lokalizacje skryptu
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

Write-Host "[INFO] Uruchamianie uslugi..." -ForegroundColor Cyan

# Uruchom proces w tle
$process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001" -PassThru -WindowStyle Hidden

# Czekaj 5 sekund na start
Start-Sleep -Seconds 5

# Sprawdz czy dziala
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8001/health" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "[OK] Usluga uruchomiona pomyslnie na http://localhost:8001" -ForegroundColor Green
        Write-Host "[INFO] Process ID: $($process.Id)" -ForegroundColor Gray
        exit 0
    }
} catch {
    Write-Host "[ERROR] Nie udalo sie uruchomic uslugi" -ForegroundColor Red
    Write-Host "[ERROR] Szczegoly: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
