#!/bin/bash

# 🔍 Skrypt diagnostyczny API - BAW Project
# Sprawdza stan backendu i możliwe problemy z dostępem

echo "=============================================="
echo "🔍 BAW API Diagnostic Tool"
echo "=============================================="
echo ""

# Kolory
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Funkcja check
check() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

echo "📋 1. Sprawdzanie statusu backendu..."
echo "------------------------------"
systemctl is-active --quiet baw-backend
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Backend (baw-backend) jest uruchomiony"
    sudo systemctl status baw-backend --no-pager -l | head -10
else
    echo -e "${RED}✗${NC} Backend (baw-backend) NIE działa!"
    echo "   Uruchom: sudo systemctl start baw-backend"
fi
echo ""

echo "📋 2. Sprawdzanie czy port 8001 nasłuchuje..."
echo "------------------------------"
PORT_CHECK=$(sudo ss -tlnp | grep :8001)
if [ -n "$PORT_CHECK" ]; then
    echo -e "${GREEN}✓${NC} Port 8001 nasłuchuje"
    echo "$PORT_CHECK"
else
    echo -e "${RED}✗${NC} Port 8001 NIE nasłuchuje!"
    echo "   Problem: Backend nie nasłuchuje na porcie 8001"
fi
echo ""

echo "📋 3. Test lokalny (localhost)..."
echo "------------------------------"
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} API odpowiada lokalnie (HTTP $RESPONSE)"
    curl -s http://localhost:8001/health | python3 -m json.tool 2>/dev/null || curl -s http://localhost:8001/health
else
    echo -e "${RED}✗${NC} API NIE odpowiada lokalnie (HTTP $RESPONSE)"
fi
echo ""

echo "📋 4. Sprawdzanie firewalla (ufw)..."
echo "------------------------------"
if command -v ufw &> /dev/null; then
    UFW_STATUS=$(sudo ufw status 2>/dev/null)
    if echo "$UFW_STATUS" | grep -q "Status: active"; then
        echo -e "${YELLOW}⚠${NC}  UFW jest aktywny"

        if echo "$UFW_STATUS" | grep -q "8001"; then
            echo -e "${GREEN}✓${NC} Port 8001 jest otwarty w ufw"
        else
            echo -e "${RED}✗${NC} Port 8001 NIE jest otwarty w ufw!"
            echo "   Napraw: sudo ufw allow 8001/tcp"
        fi

        echo ""
        echo "Aktualne reguły ufw dla portów 8000-8001:"
        sudo ufw status numbered | grep -E "8000|8001"
    else
        echo -e "${GREEN}✓${NC} UFW nie jest aktywny (nie blokuje)"
    fi
else
    echo "⊘ UFW nie jest zainstalowany"
fi
echo ""

echo "📋 5. Sprawdzanie firewalla (iptables)..."
echo "------------------------------"
IPTABLES_RULES=$(sudo iptables -L INPUT -n | grep -E "dpt:8001|dpt:8000")
if [ -n "$IPTABLES_RULES" ]; then
    echo "Znalezione reguły dla portów 8000/8001:"
    echo "$IPTABLES_RULES"
else
    echo "⊘ Brak specjalnych reguł iptables dla portów 8000/8001"
fi
echo ""

echo "📋 6. Test zewnętrzny (z serwera)..."
echo "------------------------------"
# Próba pobrania zewnętrznego IP
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "unknown")
echo "IP zewnętrzne serwera: $EXTERNAL_IP"

if [ "$EXTERNAL_IP" != "unknown" ]; then
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://$EXTERNAL_IP:8001/health 2>/dev/null)
    if [ "$RESPONSE" = "200" ]; then
        echo -e "${GREEN}✓${NC} API dostępne z zewnątrz (HTTP $RESPONSE)"
    else
        echo -e "${RED}✗${NC} API NIE dostępne z zewnątrz (HTTP $RESPONSE)"
        echo "   To wskazuje na problem z firewallem!"
    fi
else
    echo "⊘ Nie można określić zewnętrznego IP"
fi
echo ""

echo "📋 7. Sprawdzanie konfiguracji uvicorn..."
echo "------------------------------"
SERVICE_FILE="/etc/systemd/system/baw-backend.service"
if [ -f "$SERVICE_FILE" ]; then
    EXEC_LINE=$(grep "ExecStart" $SERVICE_FILE)
    echo "ExecStart: $EXEC_LINE"

    if echo "$EXEC_LINE" | grep -q "0.0.0.0"; then
        echo -e "${GREEN}✓${NC} Uvicorn nasłuchuje na wszystkich interfejsach (0.0.0.0)"
    else
        echo -e "${YELLOW}⚠${NC}  Uvicorn może nasłuchiwać tylko lokalnie!"
        echo "   Sprawdź czy jest: --host 0.0.0.0"
    fi
else
    echo -e "${RED}✗${NC} Plik service nie znaleziony: $SERVICE_FILE"
fi
echo ""

echo "=============================================="
echo "📊 PODSUMOWANIE"
echo "=============================================="
echo ""

# Diagnoza
ISSUES=0

# Check 1: Backend działa?
systemctl is-active --quiet baw-backend || ((ISSUES++))

# Check 2: Port nasłuchuje?
PORT_CHECK=$(sudo ss -tlnp | grep :8001)
[ -z "$PORT_CHECK" ] && ((ISSUES++))

# Check 3: Lokalny test
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health 2>/dev/null)
[ "$RESPONSE" != "200" ] && ((ISSUES++))

if [ $ISSUES -eq 0 ]; then
    echo -e "${GREEN}✓ Wszystko wygląda dobrze!${NC}"
    echo ""
    echo "Jeśli N8N nadal nie może połączyć się, sprawdź:"
    echo "1. Firewall na routerze/chmurze (AWS Security Groups, etc.)"
    echo "2. Konfigurację N8N (URL, metoda HTTP)"
    echo "3. Czy N8N ma dostęp do internetu"
else
    echo -e "${RED}✗ Znaleziono $ISSUES problem(y)!${NC}"
    echo ""
    echo "Zalecane akcje:"
    echo "1. Uruchom backend: sudo systemctl start baw-backend"
    echo "2. Otwórz porty: sudo ufw allow 8001/tcp && sudo ufw allow 8000/tcp"
    echo "3. Sprawdź logi: sudo journalctl -u baw-backend -n 50"
    echo ""
    echo "Możesz użyć: ./fix_firewall.sh (automatyczna naprawa)"
fi

echo ""
echo "=============================================="
echo "📝 Dodatkowe komendy diagnostyczne:"
echo "=============================================="
echo ""
echo "# Logi backendu (ostatnie 50 linii):"
echo "sudo journalctl -u baw-backend -n 50"
echo ""
echo "# Logi backendu (śledzenie na żywo):"
echo "sudo journalctl -u baw-backend -f"
echo ""
echo "# Restart backendu:"
echo "sudo systemctl restart baw-backend"
echo ""
echo "# Test z zewnętrznego komputera (Windows/Mac/Linux):"
echo "curl http://217.182.76.146:8001/health"
echo ""
