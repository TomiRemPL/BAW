#!/bin/bash
# ==============================================================================
# BAW - Stop Services Script
# Zatrzymuje Backend (UslugaDoPorownan) i Frontend (SecureDocCompare)
# ==============================================================================

set -e  # Exit on error

# Kolory dla ładnych komunikatów
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Konfiguracja
BACKEND_SCREEN="baw-backend"
FRONTEND_SCREEN="baw-frontend"

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         BAW - Zatrzymywanie Usług (Screen Mode)          ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""

# ==============================================================================
# Funkcja sprawdzająca czy screen istnieje
# ==============================================================================
check_screen_exists() {
    local screen_name=$1
    if screen -list | grep -q "$screen_name"; then
        return 0  # exists
    else
        return 1  # does not exist
    fi
}

# ==============================================================================
# Funkcja zatrzymująca screen
# ==============================================================================
stop_screen() {
    local screen_name=$1

    if check_screen_exists "$screen_name"; then
        echo -e "${YELLOW}🛑 Zatrzymuję screen: $screen_name...${NC}"
        screen -X -S "$screen_name" quit
        sleep 1

        if check_screen_exists "$screen_name"; then
            echo -e "${RED}❌ Nie udało się zatrzymać: $screen_name${NC}"
            return 1
        else
            echo -e "${GREEN}✅ Zatrzymano: $screen_name${NC}"
            return 0
        fi
    else
        echo -e "${YELLOW}⚠️  Screen '$screen_name' nie jest uruchomiony${NC}"
        return 0
    fi
}

# ==============================================================================
# Zatrzymaj usługi
# ==============================================================================

# Frontend (zatrzymuj najpierw frontend, potem backend)
stop_screen "$FRONTEND_SCREEN"

# Backend
stop_screen "$BACKEND_SCREEN"

# ==============================================================================
# Podsumowanie
# ==============================================================================
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ USŁUGI ZATRZYMANE                      ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📋 Aktualne screen sesje:${NC}"
screen -list || echo -e "${YELLOW}   Brak aktywnych sesji screen${NC}"
echo ""
echo -e "${BLUE}💡 Aby uruchomić ponownie:${NC}"
echo -e "   ${YELLOW}./start_services.sh${NC}"
echo ""
