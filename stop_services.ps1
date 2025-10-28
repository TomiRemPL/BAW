# Stop Services - PowerShell Script
# Zatrzymuje UslugaDoPorownan i SecureDocCompare

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Zatrzymywanie serwisów BAW" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Wyszukiwanie procesów uvicorn..." -ForegroundColor Green
Write-Host ""

# Znajdź procesy uvicorn na portach 8000 i 8001
$processes = @()

# Port 8001 (Backend)
$port8001Conn = Get-NetTCPConnection -LocalPort 8001 -State Listen -ErrorAction SilentlyContinue
if ($port8001Conn) {
    $pid8001 = $port8001Conn.OwningProcess
    $process8001 = Get-Process -Id $pid8001 -ErrorAction SilentlyContinue
    if ($process8001) {
        $processes += $process8001
        Write-Host "Znaleziono Backend (Port 8001):" -ForegroundColor Yellow
        Write-Host "  PID: $pid8001" -ForegroundColor Gray
        Write-Host "  Proces: $($process8001.ProcessName)" -ForegroundColor Gray
        Write-Host ""
    }
}

# Port 8000 (Frontend)
$port8000Conn = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue
if ($port8000Conn) {
    $pid8000 = $port8000Conn.OwningProcess
    $process8000 = Get-Process -Id $pid8000 -ErrorAction SilentlyContinue
    if ($process8000) {
        $processes += $process8000
        Write-Host "Znaleziono Frontend (Port 8000):" -ForegroundColor Yellow
        Write-Host "  PID: $pid8000" -ForegroundColor Gray
        Write-Host "  Proces: $($process8000.ProcessName)" -ForegroundColor Gray
        Write-Host ""
    }
}

if ($processes.Count -eq 0) {
    Write-Host "Nie znaleziono uruchomionych serwisów" -ForegroundColor Green
    Write-Host ""
    Write-Host "Naciśnij Enter aby zakończyć..." -ForegroundColor Gray
    Read-Host
    exit 0
}

# Potwierdź zatrzymanie
Write-Host "Znaleziono $($processes.Count) proces(ów) do zatrzymania" -ForegroundColor White
$confirm = Read-Host "Zatrzymać serwisy? (t/n)"

if ($confirm -ne "t") {
    Write-Host "Anulowano" -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Zatrzymywanie procesów..." -ForegroundColor Green

# Zatrzymaj procesy
foreach ($process in $processes) {
    try {
        Write-Host "Zatrzymuję PID $($process.Id) ($($process.ProcessName))..." -NoNewline -ForegroundColor Gray
        Stop-Process -Id $process.Id -Force
        Write-Host " OK" -ForegroundColor Green
    } catch {
        Write-Host " BŁĄD" -ForegroundColor Red
        Write-Host "  $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Weryfikacja..." -ForegroundColor Green
Start-Sleep -Seconds 1

# Sprawdź czy porty są wolne
$port8001Still = Get-NetTCPConnection -LocalPort 8001 -State Listen -ErrorAction SilentlyContinue
$port8000Still = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue

if (-not $port8001Still -and -not $port8000Still) {
    Write-Host "✓ Wszystkie serwisy zatrzymane" -ForegroundColor Green
} else {
    Write-Host "⚠ Niektóre porty nadal zajęte:" -ForegroundColor Yellow
    if ($port8001Still) {
        Write-Host "  Port 8001: Zajęty (PID: $($port8001Still.OwningProcess))" -ForegroundColor Yellow
    }
    if ($port8000Still) {
        Write-Host "  Port 8000: Zajęty (PID: $($port8000Still.OwningProcess))" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "Naciśnij Enter aby zakończyć..." -ForegroundColor Gray
Read-Host
