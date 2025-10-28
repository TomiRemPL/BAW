# Start Services - PowerShell Script
# Uruchamia UslugaDoPorownan (port 8001) i SecureDocCompare (port 8000)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  BAW - Document Compare Services" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Sprawdź czy jesteś w katalogu BAW
$currentDir = Get-Location
if ($currentDir.Path -notlike "*BAW*") {
    Write-Host "UWAGA: Uruchom skrypt z katalogu BAW!" -ForegroundColor Red
    Write-Host "Aktualny katalog: $currentDir" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Naciśnij Enter aby kontynuować mimo to lub Ctrl+C aby przerwać"
}

# Sprawdź czy środowisko wirtualne istnieje
if (-not (Test-Path ".\.venv\Scripts\Activate.ps1")) {
    Write-Host "BŁĄD: Nie znaleziono środowiska wirtualnego!" -ForegroundColor Red
    Write-Host "Utwórz środowisko: python -m venv .venv" -ForegroundColor Yellow
    Write-Host "Zainstaluj zależności: pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

Write-Host "[1/5] Sprawdzanie środowiska..." -ForegroundColor Green

# Aktywuj środowisko wirtualne
& .\.venv\Scripts\Activate.ps1

# Sprawdź czy Python jest dostępny
$pythonVersion = python --version 2>&1
Write-Host "Python: $pythonVersion" -ForegroundColor Gray

# Sprawdź czy uvicorn jest zainstalowany
$uvicornCheck = python -c "import uvicorn; print(uvicorn.__version__)" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "BŁĄD: Uvicorn nie jest zainstalowany!" -ForegroundColor Red
    Write-Host "Zainstaluj: pip install uvicorn" -ForegroundColor Yellow
    exit 1
}
Write-Host "Uvicorn: $uvicornCheck" -ForegroundColor Gray

Write-Host ""
Write-Host "[2/5] Sprawdzanie portów..." -ForegroundColor Green

# Sprawdź czy porty są wolne
$port8001 = Get-NetTCPConnection -LocalPort 8001 -ErrorAction SilentlyContinue
$port8000 = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue

if ($port8001) {
    Write-Host "UWAGA: Port 8001 jest zajęty!" -ForegroundColor Yellow
    Write-Host "Proces: $(Get-Process -Id $port8001.OwningProcess -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)" -ForegroundColor Gray
    $response = Read-Host "Kontynuować? (t/n)"
    if ($response -ne "t") {
        exit 1
    }
}

if ($port8000) {
    Write-Host "UWAGA: Port 8000 jest zajęty!" -ForegroundColor Yellow
    Write-Host "Proces: $(Get-Process -Id $port8000.OwningProcess -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)" -ForegroundColor Gray
    $response = Read-Host "Kontynuować? (t/n)"
    if ($response -ne "t") {
        exit 1
    }
}

Write-Host "Porty 8000 i 8001 są dostępne" -ForegroundColor Gray

Write-Host ""
Write-Host "[3/5] Uruchamianie UslugaDoPorownan (Backend - Port 8001)..." -ForegroundColor Green

# Uruchom Backend w nowym oknie PowerShell
$backendScript = @"
Set-Location '$PWD'
& .\.venv\Scripts\Activate.ps1
Set-Location UslugaDoPorownan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host '  Backend API (UslugaDoPorownan)' -ForegroundColor Cyan
Write-Host '  Port: 8001' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Uruchamianie serwera...' -ForegroundColor Green
Write-Host ''
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
"@

$backendScriptPath = Join-Path $env:TEMP "baw_backend_start.ps1"
$backendScript | Out-File -FilePath $backendScriptPath -Encoding UTF8

Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $backendScriptPath

Write-Host "Backend uruchomiony w nowym oknie" -ForegroundColor Gray
Write-Host ""

# Poczekaj 3 sekundy na start backendu
Write-Host "Czekam 3 sekundy na start backendu..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[4/5] Uruchamianie SecureDocCompare (Frontend - Port 8000)..." -ForegroundColor Green

# Uruchom Frontend w nowym oknie PowerShell
$frontendScript = @"
Set-Location '$PWD'
& .\.venv\Scripts\Activate.ps1
Set-Location SecureDocCompare
Write-Host '========================================' -ForegroundColor Cyan
Write-Host '  Frontend (SecureDocCompare)' -ForegroundColor Cyan
Write-Host '  Port: 8000' -ForegroundColor Cyan
Write-Host '========================================' -ForegroundColor Cyan
Write-Host ''
Write-Host 'Uruchamianie serwera...' -ForegroundColor Green
Write-Host ''
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"@

$frontendScriptPath = Join-Path $env:TEMP "baw_frontend_start.ps1"
$frontendScript | Out-File -FilePath $frontendScriptPath -Encoding UTF8

Start-Process powershell -ArgumentList "-NoExit", "-ExecutionPolicy", "Bypass", "-File", $frontendScriptPath

Write-Host "Frontend uruchomiony w nowym oknie" -ForegroundColor Gray
Write-Host ""

# Poczekaj 3 sekundy na start frontendu
Write-Host "Czekam 3 sekundy na start frontendu..." -ForegroundColor Gray
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "[5/5] Sprawdzanie statusu serwisów..." -ForegroundColor Green
Start-Sleep -Seconds 2

# Sprawdź health endpoints
try {
    $backendHealth = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get -TimeoutSec 5
    Write-Host "✓ Backend (8001): " -NoNewline -ForegroundColor Green
    Write-Host "OK - $($backendHealth.status)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Backend (8001): " -NoNewline -ForegroundColor Red
    Write-Host "Błąd połączenia" -ForegroundColor Gray
}

try {
    $frontendHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "✓ Frontend (8000): " -NoNewline -ForegroundColor Green
    Write-Host "OK - $($frontendHealth.status)" -ForegroundColor Gray
} catch {
    Write-Host "✗ Frontend (8000): " -NoNewline -ForegroundColor Red
    Write-Host "Błąd połączenia" -ForegroundColor Gray
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Serwisy uruchomione!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8001" -ForegroundColor Yellow
Write-Host "API Docs:     " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8001/docs" -ForegroundColor Yellow
Write-Host ""
Write-Host "Frontend:     " -NoNewline -ForegroundColor White
Write-Host "http://localhost:8000" -ForegroundColor Yellow
Write-Host ""
Write-Host "Aby zatrzymać serwisy:" -ForegroundColor White
Write-Host "  PowerShell: .\stop_services.ps1" -ForegroundColor Gray
Write-Host "  Lub zamknij okna terminali" -ForegroundColor Gray
Write-Host ""
Write-Host "Logi widoczne w osobnych oknach terminali" -ForegroundColor Gray
Write-Host ""

# Opcjonalnie otwórz przeglądarkę
$openBrowser = Read-Host "Otworzyć przeglądarkę? (t/n)"
if ($openBrowser -eq "t") {
    Start-Process "http://localhost:8000"
}

Write-Host ""
Write-Host "Naciśnij Enter aby zamknąć to okno..." -ForegroundColor Gray
Read-Host
