#!/bin/bash
# ==============================================================================
# BAW - Status Services Script
# Sprawdza status Backend (UslugaDoPorownan) i Frontend (SecureDocCompare)
# ==============================================================================

# Kolory dla ładnych komunikatów
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Konfiguracja
BACKEND_SCREEN="baw-backend"
FRONTEND_SCREEN="baw-frontend"
BACKEND_PORT=8001
FRONTEND_PORT=8000
BACKEND_URL="http://localhost:$BACKEND_PORT"
FRONTEND_URL="http://localhost:$FRONTEND_PORT"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║            BAW - Status Usług (Screen Mode)              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# Funkcja sprawdzająca czy screen istnieje
# ==============================================================================
check_screen_exists() {
    local screen_name=$1
    if screen -list 2>/dev/null | grep -q "$screen_name"; then
        return 0  # exists
    else
        return 1  # does not exist
    fi
}

# ==============================================================================
# Funkcja sprawdzająca czy port jest otwarty
# ==============================================================================
check_port() {
    local port=$1
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        return 0  # port zajęty/otwarty
    elif netstat -tlnp 2>/dev/null | grep -q ":$port "; then
        return 0  # fallback do netstat
    else
        return 1  # port zamknięty
    fi
}

# ==============================================================================
# Funkcja sprawdzająca health endpoint
# ==============================================================================
check_health() {
    local url=$1
    local response=$(curl -s -o /dev/null -w "%{http_code}" "$url/health" 2>/dev/null)

    if [ "$response" = "200" ]; then
        return 0  # healthy
    else
        return 1  # not healthy
    fi
}

# ==============================================================================
# Funkcja wyświetlająca status serwisu
# ==============================================================================
show_service_status() {
    local service_name=$1
    local screen_name=$2
    local port=$3
    local url=$4

    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}📦 $service_name${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

    # Screen status
    if check_screen_exists "$screen_name"; then
        echo -e "   Screen Session:  ${GREEN}✅ Aktywny${NC} ($screen_name)"
    else
        echo -e "   Screen Session:  ${RED}❌ Nieaktywny${NC}"
    fi

    # Port status
    if check_port $port; then
        echo -e "   Port $port:       ${GREEN}✅ Otwarty${NC}"
    else
        echo -e "   Port $port:       ${RED}❌ Zamknięty${NC}"
    fi

    # Health check
    if check_health "$url"; then
        echo -e "   Health Check:    ${GREEN}✅ Zdrowy${NC} ($url/health)"

        # Pobierz dodatkowe info z health endpoint
        health_data=$(curl -s "$url/health" 2>/dev/null)
        if [ -n "$health_data" ]; then
            status=$(echo "$health_data" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
            timestamp=$(echo "$health_data" | grep -o '"timestamp":"[^"]*"' | cut -d'"' -f4)
            if [ -n "$status" ]; then
                echo -e "   Status:          ${BLUE}$status${NC}"
            fi
            if [ -n "$timestamp" ]; then
                echo -e "   Timestamp:       ${BLUE}$timestamp${NC}"
            fi
        fi
    else
        echo -e "   Health Check:    ${RED}❌ Niedostępny${NC}"
    fi

    echo ""
}

# ==============================================================================
# Sprawdź status obu usług
# ==============================================================================

show_service_status "Backend (UslugaDoPorownan)" "$BACKEND_SCREEN" "$BACKEND_PORT" "$BACKEND_URL"
show_service_status "Frontend (SecureDocCompare)" "$FRONTEND_SCREEN" "$FRONTEND_PORT" "$FRONTEND_URL"

# ==============================================================================
# Wszystkie screen sesje
# ==============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}📋 Wszystkie Screen Sesje${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if screen -list 2>/dev/null | grep -q "Socket"; then
    screen -list | grep -E "baw-|Socket" || echo -e "${YELLOW}   Brak sesji BAW${NC}"
else
    echo -e "${YELLOW}   Brak aktywnych sesji screen${NC}"
fi

echo ""

# ==============================================================================
# Zajęte porty
# ==============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🔌 Zajęte Porty (8000, 8001)${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

if command -v ss &> /dev/null; then
    ss -tlnp 2>/dev/null | grep -E ":8000 |:8001 " || echo -e "${YELLOW}   Brak nasłuchujących procesów na portach 8000/8001${NC}"
elif command -v netstat &> /dev/null; then
    netstat -tlnp 2>/dev/null | grep -E ":8000 |:8001 " || echo -e "${YELLOW}   Brak nasłuchujących procesów na portach 8000/8001${NC}"
else
    echo -e "${YELLOW}   Narzędzia ss/netstat niedostępne${NC}"
fi

echo ""

# ==============================================================================
# Podsumowanie i akcje
# ==============================================================================
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}💡 Dostępne Akcje${NC}"
echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

# Sprawdź czy którakolwiek usługa działa
backend_running=false
frontend_running=false

if check_screen_exists "$BACKEND_SCREEN"; then
    backend_running=true
fi

if check_screen_exists "$FRONTEND_SCREEN"; then
    frontend_running=true
fi

if [ "$backend_running" = true ] && [ "$frontend_running" = true ]; then
    echo -e "   ${GREEN}✅ Wszystkie usługi działają${NC}"
    echo -e "   Zatrzymaj:           ${YELLOW}./stop_services.sh${NC}"
    echo -e "   Podłącz do backendu: ${YELLOW}screen -r $BACKEND_SCREEN${NC}"
    echo -e "   Podłącz do frontendu:${YELLOW}screen -r $FRONTEND_SCREEN${NC}"
    echo -e "   Odłącz (w screen):   ${YELLOW}Ctrl+A, D${NC}"
elif [ "$backend_running" = false ] && [ "$frontend_running" = false ]; then
    echo -e "   ${RED}❌ Żadna usługa nie działa${NC}"
    echo -e "   Uruchom:             ${YELLOW}./start_services.sh${NC}"
else
    echo -e "   ${YELLOW}⚠️  Tylko część usług działa${NC}"
    echo -e "   Zatrzymaj:           ${YELLOW}./stop_services.sh${NC}"
    echo -e "   Uruchom:             ${YELLOW}./start_services.sh${NC}"
fi

echo ""
