# Check Services - PowerShell Script
# Sprawdza status UslugaDoPorownan i SecureDocCompare

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Status serwisów BAW" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "[1/3] Sprawdzanie portów..." -ForegroundColor Green
Write-Host ""

# Sprawdź porty
$port8001 = Get-NetTCPConnection -LocalPort 8001 -State Listen -ErrorAction SilentlyContinue
$port8000 = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

if ($port8001) {
    $process8001 = Get-Process -Id $port8001.OwningProcess -ErrorAction SilentlyContinue
    Write-Host "Backend (Port 8001): " -NoNewline -ForegroundColor White
    Write-Host "URUCHOMIONY" -ForegroundColor Green
    Write-Host "  PID: $($port8001.OwningProcess)" -ForegroundColor Gray
    Write-Host "  Proces: $($process8001.ProcessName)" -ForegroundColor Gray
    Write-Host "  Czas uruchomienia: $($process8001.StartTime)" -ForegroundColor Gray
} else {
    Write-Host "Backend (Port 8001): " -NoNewline -ForegroundColor White
    Write-Host "ZATRZYMANY" -ForegroundColor Red
}

Write-Host ""

if ($port8000) {
    $process8000 = Get-Process -Id $port8000.OwningProcess -ErrorAction SilentlyContinue
    Write-Host "Frontend (Port 8000): " -NoNewline -ForegroundColor White
    Write-Host "URUCHOMIONY" -ForegroundColor Green
    Write-Host "  PID: $($port8000.OwningProcess)" -ForegroundColor Gray
    Write-Host "  Proces: $($process8000.ProcessName)" -ForegroundColor Gray
    Write-Host "  Czas uruchomienia: $($process8000.StartTime)" -ForegroundColor Gray
} else {
    Write-Host "Frontend (Port 8000): " -NoNewline -ForegroundColor White
    Write-Host "ZATRZYMANY" -ForegroundColor Red
}

Write-Host ""
Write-Host "[2/3] Sprawdzanie health endpoints..." -ForegroundColor Green
Write-Host ""

# Sprawdź health endpoints
if ($port8001) {
    try {
        $backendHealth = Invoke-RestMethod -Uri "http://localhost:8001/health" -Method Get -TimeoutSec 5
        Write-Host "Backend Health: " -NoNewline -ForegroundColor White
        Write-Host "OK" -ForegroundColor Green
        Write-Host "  Status: $($backendHealth.status)" -ForegroundColor Gray

        if ($backendHealth.statistics) {
            Write-Host "  Statystyki:" -ForegroundColor Gray
            Write-Host "    - Dokumenty: $($backendHealth.statistics.total_documents)" -ForegroundColor Gray
            Write-Host "    - Procesy: $($backendHealth.statistics.total_processes)" -ForegroundColor Gray
            Write-Host "    - Podsumowania: $($backendHealth.statistics.total_summaries)" -ForegroundColor Gray
            Write-Host "    - Oczekujące: $($backendHealth.statistics.pending_summaries)" -ForegroundColor Gray
            Write-Host "    - Zatwierdzone: $($backendHealth.statistics.approved_summaries)" -ForegroundColor Gray
        }
    } catch {
        Write-Host "Backend Health: " -NoNewline -ForegroundColor White
        Write-Host "BŁĄD" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Backend Health: " -NoNewline -ForegroundColor White
    Write-Host "NIEDOSTĘPNY (serwis zatrzymany)" -ForegroundColor Yellow
}

Write-Host ""

if ($port8000) {
    try {
        $frontendHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
        Write-Host "Frontend Health: " -NoNewline -ForegroundColor White
        Write-Host "OK" -ForegroundColor Green
        Write-Host "  Status: $($frontendHealth.status)" -ForegroundColor Gray
        Write-Host "  Backend API: $($frontendHealth.backend_api)" -ForegroundColor Gray
    } catch {
        Write-Host "Frontend Health: " -NoNewline -ForegroundColor White
        Write-Host "BŁĄD" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    }
} else {
    Write-Host "Frontend Health: " -NoNewline -ForegroundColor White
    Write-Host "NIEDOSTĘPNY (serwis zatrzymany)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Test połączenia..." -ForegroundColor Green
Write-Host ""

# Test dostępności przez curl/wget (jeśli dostępne)
if ($port8001) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8001/" -Method Get -TimeoutSec 5 -UseBasicParsing
        Write-Host "Backend API (/):" -NoNewline -ForegroundColor White
        Write-Host " $($response.StatusCode) OK" -ForegroundColor Green
    } catch {
        Write-Host "Backend API (/):" -NoNewline -ForegroundColor White
        Write-Host " BŁĄD" -ForegroundColor Red
    }
}

if ($port8000) {
    try {
        $response = Invoke-WebRequest -Uri "http://localhost:8000/" -Method Get -TimeoutSec 5 -UseBasicParsing
        Write-Host "Frontend (/):" -NoNewline -ForegroundColor White
        Write-Host " $($response.StatusCode) OK" -ForegroundColor Green
    } catch {
        Write-Host "Frontend (/):" -NoNewline -ForegroundColor White
        Write-Host " BŁĄD" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Podsumowanie
if ($port8001 -and $port8000) {
    Write-Host "  Status: WSZYSTKO DZIAŁA" -ForegroundColor Green
    Write-Host ""
    Write-Host "Adresy:" -ForegroundColor White
    Write-Host "  Backend:  http://localhost:8001" -ForegroundColor Yellow
    Write-Host "  Docs:     http://localhost:8001/docs" -ForegroundColor Yellow
    Write-Host "  Frontend: http://localhost:8000" -ForegroundColor Yellow
} elseif ($port8001 -or $port8000) {
    Write-Host "  Status: CZĘŚCIOWO URUCHOMIONE" -ForegroundColor Yellow
    Write-Host ""
    if (-not $port8001) {
        Write-Host "⚠ Backend jest zatrzymany" -ForegroundColor Yellow
        Write-Host "  Uruchom: .\start_services.ps1" -ForegroundColor Gray
    }
    if (-not $port8000) {
        Write-Host "⚠ Frontend jest zatrzymany" -ForegroundColor Yellow
        Write-Host "  Uruchom: .\start_services.ps1" -ForegroundColor Gray
    }
} else {
    Write-Host "  Status: WSZYSTKO ZATRZYMANE" -ForegroundColor Red
    Write-Host ""
    Write-Host "Uruchom serwisy:" -ForegroundColor White
    Write-Host "  PowerShell: .\start_services.ps1" -ForegroundColor Gray
    Write-Host "  Batch:      start_services.bat" -ForegroundColor Gray
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Naciśnij Enter aby zakończyć..." -ForegroundColor Gray
Read-Host
