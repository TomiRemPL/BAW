#!/bin/bash

# 🔧 Skrypt naprawczy Firewall - BAW Project
# Automatycznie otwiera porty 8000 i 8001 dla API

echo "=============================================="
echo "🔧 BAW Firewall Fix Tool"
echo "=============================================="
echo ""

# Kolory
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Sprawdź czy jesteś rootem
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}✗ Ten skrypt wymaga uprawnień root${NC}"
    echo "Uruchom: sudo ./fix_firewall.sh"
    exit 1
fi

echo -e "${BLUE}Ten skrypt otworzy porty 8000 i 8001 w firewallu.${NC}"
echo ""
read -p "Czy kontynuować? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Anulowano."
    exit 0
fi

echo ""
echo "=============================================="
echo "📋 Krok 1: Sprawdzanie UFW"
echo "=============================================="

if command -v ufw &> /dev/null; then
    echo "✓ UFW jest zainstalowany"

    UFW_STATUS=$(ufw status 2>/dev/null)
    if echo "$UFW_STATUS" | grep -q "Status: active"; then
        echo "✓ UFW jest aktywny"
        echo ""
        echo "Otwieranie portów w UFW..."

        # Port 8001 (Backend API)
        if echo "$UFW_STATUS" | grep -q "8001"; then
            echo -e "${GREEN}✓${NC} Port 8001 już otwarty"
        else
            ufw allow 8001/tcp
            echo -e "${GREEN}✓${NC} Otworzono port 8001/tcp"
        fi

        # Port 8000 (Frontend)
        if echo "$UFW_STATUS" | grep -q "8000"; then
            echo -e "${GREEN}✓${NC} Port 8000 już otwarty"
        else
            ufw allow 8000/tcp
            echo -e "${GREEN}✓${NC} Otworzono port 8000/tcp"
        fi

        # Reload UFW
        echo ""
        echo "Przeładowywanie UFW..."
        ufw reload
        echo -e "${GREEN}✓${NC} UFW przeładowany"

        echo ""
        echo "Aktualne reguły dla portów 8000-8001:"
        ufw status | grep -E "8000|8001"

    else
        echo "⊘ UFW nie jest aktywny - nie wymaga konfiguracji"
    fi
else
    echo "⊘ UFW nie jest zainstalowany"
fi

echo ""
echo "=============================================="
echo "📋 Krok 2: Sprawdzanie iptables"
echo "=============================================="

# Sprawdź czy iptables ma jakieś reguły blokujące
IPTABLES_INPUT=$(iptables -L INPUT -n | grep -E "DROP|REJECT")

if [ -n "$IPTABLES_INPUT" ]; then
    echo "⚠  Znaleziono reguły blokujące w iptables"
    echo ""
    echo "Dodawanie reguł ACCEPT dla portów 8000 i 8001..."

    # Sprawdź czy reguły już istnieją
    if ! iptables -C INPUT -p tcp --dport 8001 -j ACCEPT 2>/dev/null; then
        iptables -I INPUT -p tcp --dport 8001 -j ACCEPT
        echo -e "${GREEN}✓${NC} Dodano regułę iptables dla portu 8001"
    else
        echo -e "${GREEN}✓${NC} Reguła dla portu 8001 już istnieje"
    fi

    if ! iptables -C INPUT -p tcp --dport 8000 -j ACCEPT 2>/dev/null; then
        iptables -I INPUT -p tcp --dport 8000 -j ACCEPT
        echo -e "${GREEN}✓${NC} Dodano regułę iptables dla portu 8000"
    else
        echo -e "${GREEN}✓${NC} Reguła dla portu 8000 już istnieje"
    fi

    # Zapisz reguły (Debian/Ubuntu)
    echo ""
    echo "Zapisywanie reguł iptables..."
    if command -v iptables-save &> /dev/null; then
        mkdir -p /etc/iptables
        iptables-save > /etc/iptables/rules.v4
        echo -e "${GREEN}✓${NC} Reguły iptables zapisane"
    else
        echo -e "${YELLOW}⚠${NC}  iptables-save niedostępny - reguły mogą zniknąć po restarcie"
    fi
else
    echo "✓ Brak blokujących reguł iptables"
fi

echo ""
echo "=============================================="
echo "📋 Krok 3: Sprawdzanie backendu"
echo "=============================================="

systemctl is-active --quiet baw-backend
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Backend działa"
else
    echo -e "${YELLOW}⚠${NC}  Backend nie działa, uruchamiam..."
    systemctl start baw-backend
    sleep 2

    systemctl is-active --quiet baw-backend
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓${NC} Backend uruchomiony"
    else
        echo -e "${RED}✗${NC} Nie udało się uruchomić backendu!"
        echo "Sprawdź: sudo journalctl -u baw-backend -n 50"
    fi
fi

echo ""
echo "=============================================="
echo "📋 Krok 4: Testy połączenia"
echo "=============================================="

echo "Test 1: localhost..."
sleep 2
RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health 2>/dev/null)
if [ "$RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} API odpowiada lokalnie (HTTP $RESPONSE)"
else
    echo -e "${RED}✗${NC} API nie odpowiada lokalnie (HTTP $RESPONSE)"
fi

echo ""
echo "Test 2: zewnętrzne IP..."
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null)
if [ -n "$EXTERNAL_IP" ]; then
    echo "IP serwera: $EXTERNAL_IP"
    RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://$EXTERNAL_IP:8001/health 2>/dev/null)
    if [ "$RESPONSE" = "200" ]; then
        echo -e "${GREEN}✓${NC} API dostępne z zewnątrz (HTTP $RESPONSE)"
    else
        echo -e "${YELLOW}⚠${NC}  API nie odpowiada z zewnątrz (HTTP $RESPONSE)"
        echo "   To może być problem z routerem/cloud firewall"
    fi
fi

echo ""
echo "=============================================="
echo "✅ ZAKOŃCZONO"
echo "=============================================="
echo ""
echo "Porty 8000 i 8001 powinny być teraz dostępne."
echo ""
echo "📝 Następne kroki:"
echo ""
echo "1. Test z N8N:"
echo "   URL: http://217.182.76.146:8001/health"
echo "   Metoda: GET"
echo ""
echo "2. Test z przeglądarki:"
echo "   http://217.182.76.146:8000 (Frontend)"
echo ""
echo "3. Test z curl (z twojego komputera):"
echo "   curl http://217.182.76.146:8001/health"
echo ""
echo "4. Jeśli nadal nie działa, sprawdź:"
echo "   - Cloud firewall (AWS Security Groups, etc.)"
echo "   - Router firewall"
echo "   - Logi: sudo journalctl -u baw-backend -n 50"
echo ""
