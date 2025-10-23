#!/bin/bash

# 🔧 Skrypt konfiguracji Nginx Reverse Proxy dla BAW API
# Autor: BAW Project
# Data: 2025-10-23
# Cel: Konfiguruje Nginx jako reverse proxy na porcie 80 dla backendu na porcie 8001

set -e  # Zatrzymaj przy błędzie

# Kolory
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "=============================================="
echo "🔧 Konfiguracja Nginx Reverse Proxy - BAW API"
echo "=============================================="
echo ""

# Sprawdź czy jesteś rootem (dla apt install)
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}⚠  Ten skrypt wymaga uprawnień sudo${NC}"
    echo "Niektóre operacje będą wymagały hasła."
    echo ""
fi

# ========================================
# KROK 1: Instalacja Nginx (jeśli brak)
# ========================================
echo -e "${BLUE}📋 Krok 1: Sprawdzanie Nginx...${NC}"

if ! command -v nginx &> /dev/null; then
    echo "Nginx nie jest zainstalowany. Instaluję..."
    sudo apt update
    sudo apt install -y nginx
    echo -e "${GREEN}✓${NC} Nginx zainstalowany"
else
    echo -e "${GREEN}✓${NC} Nginx już zainstalowany"
fi

# ========================================
# KROK 2: Tworzenie konfiguracji
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 2: Tworzenie konfiguracji reverse proxy...${NC}"

sudo tee /etc/nginx/sites-available/baw-api > /dev/null <<'EOF'
server {
    listen 80;
    server_name _;

    # Backend API endpoints
    location /api/ {
        proxy_pass http://localhost:8001/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeouty dla długich operacji (upload PDF, konwersja)
        proxy_connect_timeout 120s;
        proxy_send_timeout 120s;
        proxy_read_timeout 120s;

        # Buffer settings dla dużych plików
        client_max_body_size 50M;
        proxy_buffering off;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://localhost:8001/health;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Swagger UI dokumentacja
    location /docs {
        proxy_pass http://localhost:8001/docs;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # ReDoc dokumentacja
    location /redoc {
        proxy_pass http://localhost:8001/redoc;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # OpenAPI schema
    location /openapi.json {
        proxy_pass http://localhost:8001/openapi.json;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Root endpoint
    location = / {
        proxy_pass http://localhost:8001/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Logi
    access_log /var/log/nginx/baw-api-access.log;
    error_log /var/log/nginx/baw-api-error.log;
}
EOF

echo -e "${GREEN}✓${NC} Konfiguracja utworzona: /etc/nginx/sites-available/baw-api"

# ========================================
# KROK 3: Aktywacja konfiguracji
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 3: Aktywacja konfiguracji...${NC}"

# Usuń domyślną konfigurację (jeśli istnieje)
if [ -f /etc/nginx/sites-enabled/default ]; then
    sudo rm /etc/nginx/sites-enabled/default
    echo -e "${GREEN}✓${NC} Usunięto domyślną konfigurację"
fi

# Aktywuj naszą konfigurację
sudo ln -sf /etc/nginx/sites-available/baw-api /etc/nginx/sites-enabled/
echo -e "${GREEN}✓${NC} Konfiguracja aktywowana"

# ========================================
# KROK 4: Test konfiguracji
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 4: Testowanie konfiguracji Nginx...${NC}"

if sudo nginx -t 2>&1 | grep -q "successful"; then
    echo -e "${GREEN}✓${NC} Konfiguracja Nginx poprawna"
else
    echo -e "${RED}✗${NC} Błąd w konfiguracji Nginx!"
    sudo nginx -t
    exit 1
fi

# ========================================
# KROK 5: Restart Nginx
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 5: Restart Nginx...${NC}"

sudo systemctl restart nginx
sudo systemctl enable nginx

if sudo systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✓${NC} Nginx uruchomiony i działa"
else
    echo -e "${RED}✗${NC} Nginx nie działa!"
    sudo systemctl status nginx --no-pager -l
    exit 1
fi

# ========================================
# KROK 6: Sprawdzenie backendu
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 6: Sprawdzanie backendu...${NC}"

# Sprawdź czy backend odpowiada
BACKEND_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8001/health 2>/dev/null || echo "000")

if [ "$BACKEND_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Backend odpowiada (port 8001)"
else
    echo -e "${YELLOW}⚠${NC}  Backend nie odpowiada (HTTP $BACKEND_RESPONSE)"
    echo "    Upewnij się, że backend działa:"
    echo "    sudo systemctl status baw-backend"
fi

# ========================================
# KROK 7: Testy połączenia
# ========================================
echo ""
echo -e "${BLUE}📋 Krok 7: Testy połączenia...${NC}"

# Test 1: Localhost przez Nginx
echo ""
echo "Test 1: Health check przez Nginx (localhost:80)"
NGINX_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/health 2>/dev/null || echo "000")

if [ "$NGINX_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Nginx proxy działa (HTTP $NGINX_RESPONSE)"
    echo "Odpowiedź:"
    curl -s http://localhost/health | head -5
else
    echo -e "${RED}✗${NC} Nginx proxy nie działa (HTTP $NGINX_RESPONSE)"
fi

# Test 2: Dokumentacja
echo ""
echo "Test 2: Swagger docs"
DOCS_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/docs 2>/dev/null || echo "000")

if [ "$DOCS_RESPONSE" = "200" ]; then
    echo -e "${GREEN}✓${NC} Dokumentacja dostępna (HTTP $DOCS_RESPONSE)"
else
    echo -e "${YELLOW}⚠${NC}  Dokumentacja niedostępna (HTTP $DOCS_RESPONSE)"
fi

# Test 3: Zewnętrzne IP
echo ""
echo "Test 3: Dostęp z zewnątrz"
EXTERNAL_IP=$(curl -s ifconfig.me 2>/dev/null || curl -s icanhazip.com 2>/dev/null || echo "unknown")

if [ "$EXTERNAL_IP" != "unknown" ]; then
    echo "Zewnętrzne IP serwera: $EXTERNAL_IP"
    echo "Test z serwera (loopback przez IP)..."

    EXTERNAL_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 http://$EXTERNAL_IP/health 2>/dev/null || echo "000")

    if [ "$EXTERNAL_RESPONSE" = "200" ]; then
        echo -e "${GREEN}✓${NC} API dostępne z zewnątrz (HTTP $EXTERNAL_RESPONSE)"
    else
        echo -e "${YELLOW}⚠${NC}  API nie odpowiada z zewnątrz (HTTP $EXTERNAL_RESPONSE)"
        echo "    To może być normalne - sprawdź z innego komputera"
    fi
else
    echo "⊘ Nie można określić zewnętrznego IP"
fi

# ========================================
# PODSUMOWANIE
# ========================================
echo ""
echo "=============================================="
echo "✅ KONFIGURACJA ZAKOŃCZONA"
echo "=============================================="
echo ""

if [ "$NGINX_RESPONSE" = "200" ]; then
    echo -e "${GREEN}🎉 Nginx reverse proxy działa poprawnie!${NC}"
    echo ""
    echo "📝 Nowe URL-e API (port 80 - nie blokowany przez proxy):"
    echo ""
    echo "  Health check:"
    echo "    http://217.182.76.146/health"
    echo ""
    echo "  Upload dokumentów:"
    echo "    POST http://217.182.76.146/api/documents/upload"
    echo ""
    echo "  Rozpocznij przetwarzanie:"
    echo "    POST http://217.182.76.146/api/process"
    echo ""
    echo "  Sprawdź status:"
    echo "    GET http://217.182.76.146/api/status/{process_id}"
    echo ""
    echo "  Pobierz wyniki:"
    echo "    GET http://217.182.76.146/api/result/{process_id}/full"
    echo ""
    echo "🌐 Dokumentacja API (Swagger):"
    echo "    http://217.182.76.146/docs"
    echo ""
    echo "🔧 Testy z twojego komputera (Windows PowerShell):"
    echo "    curl http://217.182.76.146/health"
    echo ""
    echo "📋 Użyj tych URL-i w N8N - bez ':8001' na końcu!"
    echo ""
else
    echo -e "${RED}⚠  Problem z konfiguracją!${NC}"
    echo ""
    echo "Sprawdź:"
    echo "1. Czy backend działa:"
    echo "   sudo systemctl status baw-backend"
    echo ""
    echo "2. Logi Nginx:"
    echo "   sudo tail -f /var/log/nginx/baw-api-error.log"
    echo ""
    echo "3. Logi backendu:"
    echo "   sudo journalctl -u baw-backend -n 50"
fi

echo ""
echo "=============================================="
echo "📚 Dodatkowe komendy:"
echo "=============================================="
echo ""
echo "# Restart Nginx:"
echo "sudo systemctl restart nginx"
echo ""
echo "# Status Nginx:"
echo "sudo systemctl status nginx"
echo ""
echo "# Logi Nginx (błędy):"
echo "sudo tail -f /var/log/nginx/baw-api-error.log"
echo ""
echo "# Logi Nginx (access):"
echo "sudo tail -f /var/log/nginx/baw-api-access.log"
echo ""
echo "# Test konfiguracji:"
echo "sudo nginx -t"
echo ""
echo "# Restart backendu:"
echo "sudo systemctl restart baw-backend"
echo ""

exit 0
