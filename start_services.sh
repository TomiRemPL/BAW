#!/bin/bash
# ==============================================================================
# BAW - Start Services Script
# Uruchamia Backend (UslugaDoPorownan) i Frontend (SecureDocCompare) w screen
# ==============================================================================

set -e  # Exit on error

# Kolory dla ładnych komunikatów
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Konfiguracja
PROJECT_ROOT="/home/debian/hack/BAW"
VENV_PATH="$PROJECT_ROOT/.venv"
BACKEND_DIR="$PROJECT_ROOT/UslugaDoPorownan"
FRONTEND_DIR="$PROJECT_ROOT/SecureDocCompare"
BACKEND_SCREEN="baw-backend"
FRONTEND_SCREEN="baw-frontend"
BACKEND_PORT=8001
FRONTEND_PORT=8000

echo -e "${BLUE}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         BAW - Uruchamianie Usług (Screen Mode)           ║${NC}"
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
# Funkcja sprawdzająca czy port jest zajęty
# ==============================================================================
check_port() {
    local port=$1
    if ss -tlnp 2>/dev/null | grep -q ":$port "; then
        return 0  # port zajęty
    else
        return 1  # port wolny
    fi
}

# ==============================================================================
# Sprawdzenia wstępne
# ==============================================================================
echo -e "${YELLOW}📋 Sprawdzenia wstępne...${NC}"

# Sprawdź czy jesteśmy w odpowiednim katalogu lub przejdź do niego
if [ ! -d "$PROJECT_ROOT" ]; then
    echo -e "${RED}❌ Błąd: Katalog projektu nie istnieje: $PROJECT_ROOT${NC}"
    exit 1
fi

# Sprawdź czy virtualenv istnieje
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${RED}❌ Błąd: Virtualenv nie istnieje: $VENV_PATH${NC}"
    echo -e "${YELLOW}   Uruchom: python -m venv $VENV_PATH${NC}"
    exit 1
fi

# Sprawdź czy screen jest zainstalowany
if ! command -v screen &> /dev/null; then
    echo -e "${RED}❌ Błąd: 'screen' nie jest zainstalowany${NC}"
    echo -e "${YELLOW}   Zainstaluj: sudo apt install screen${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Wszystkie wymagania spełnione${NC}"
echo ""

# ==============================================================================
# Backend (UslugaDoPorownan)
# ==============================================================================
echo -e "${YELLOW}🔧 Backend (UslugaDoPorownan) - port $BACKEND_PORT...${NC}"

# Sprawdź czy screen już istnieje
if check_screen_exists "$BACKEND_SCREEN"; then
    echo -e "${YELLOW}⚠️  Screen '$BACKEND_SCREEN' już istnieje${NC}"
    echo -e "${YELLOW}   Zatrzymaj go najpierw: screen -X -S $BACKEND_SCREEN quit${NC}"
    echo -e "${YELLOW}   Lub użyj: ./stop_services.sh${NC}"
    exit 1
fi

# Sprawdź czy port jest zajęty
if check_port $BACKEND_PORT; then
    echo -e "${RED}❌ Port $BACKEND_PORT jest już zajęty${NC}"
    echo -e "${YELLOW}   Sprawdź: sudo ss -tlnp | grep $BACKEND_PORT${NC}"
    exit 1
fi

# Uruchom backend w screen
echo -e "${BLUE}   Starting backend screen session...${NC}"
screen -dmS "$BACKEND_SCREEN" bash -c "
    cd $PROJECT_ROOT && \
    source $VENV_PATH/bin/activate && \
    cd $BACKEND_DIR && \
    echo 'Backend starting on port $BACKEND_PORT...' && \
    uvicorn main:app --host 0.0.0.0 --port $BACKEND_PORT
"

sleep 2  # Poczekaj chwilę na start

# Sprawdź czy wystartował
if check_screen_exists "$BACKEND_SCREEN"; then
    echo -e "${GREEN}✅ Backend uruchomiony w screen: $BACKEND_SCREEN${NC}"
else
    echo -e "${RED}❌ Błąd uruchamiania backendu${NC}"
    exit 1
fi

# ==============================================================================
# Frontend (SecureDocCompare)
# ==============================================================================
echo ""
echo -e "${YELLOW}🌐 Frontend (SecureDocCompare) - port $FRONTEND_PORT...${NC}"

# Sprawdź czy screen już istnieje
if check_screen_exists "$FRONTEND_SCREEN"; then
    echo -e "${YELLOW}⚠️  Screen '$FRONTEND_SCREEN' już istnieje${NC}"
    echo -e "${YELLOW}   Zatrzymuję backend i kończę...${NC}"
    screen -X -S "$BACKEND_SCREEN" quit
    exit 1
fi

# Sprawdź czy port jest zajęty
if check_port $FRONTEND_PORT; then
    echo -e "${RED}❌ Port $FRONTEND_PORT jest już zajęty${NC}"
    echo -e "${YELLOW}   Zatrzymuję backend i kończę...${NC}"
    screen -X -S "$BACKEND_SCREEN" quit
    exit 1
fi

# Uruchom frontend w screen
echo -e "${BLUE}   Starting frontend screen session...${NC}"
screen -dmS "$FRONTEND_SCREEN" bash -c "
    cd $PROJECT_ROOT && \
    source $VENV_PATH/bin/activate && \
    cd $FRONTEND_DIR && \
    echo 'Frontend starting on port $FRONTEND_PORT...' && \
    uvicorn main:app --host 0.0.0.0 --port $FRONTEND_PORT
"

sleep 2  # Poczekaj chwilę na start

# Sprawdź czy wystartował
if check_screen_exists "$FRONTEND_SCREEN"; then
    echo -e "${GREEN}✅ Frontend uruchomiony w screen: $FRONTEND_SCREEN${NC}"
else
    echo -e "${RED}❌ Błąd uruchamiania frontendu${NC}"
    echo -e "${YELLOW}   Zatrzymuję backend...${NC}"
    screen -X -S "$BACKEND_SCREEN" quit
    exit 1
fi

# ==============================================================================
# Podsumowanie i instrukcje
# ==============================================================================
echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                  ✅ USŁUGI URUCHOMIONE                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${BLUE}📍 Dostępne endpointy:${NC}"
echo -e "   Backend API:  http://localhost:$BACKEND_PORT"
echo -e "   Frontend:     http://localhost:$FRONTEND_PORT"
echo ""
echo -e "${BLUE}🖥️  Screen sesje:${NC}"
echo -e "   Backend:  $BACKEND_SCREEN"
echo -e "   Frontend: $FRONTEND_SCREEN"
echo ""
echo -e "${BLUE}📋 Przydatne komendy:${NC}"
echo -e "   Lista screenów:          ${YELLOW}screen -list${NC}"
echo -e "   Podłącz do backendu:     ${YELLOW}screen -r $BACKEND_SCREEN${NC}"
echo -e "   Podłącz do frontendu:    ${YELLOW}screen -r $FRONTEND_SCREEN${NC}"
echo -e "   Odłącz się (w screen):   ${YELLOW}Ctrl+A, D${NC}"
echo -e "   Zatrzymaj usługi:        ${YELLOW}./stop_services.sh${NC}"
echo -e "   Status usług:            ${YELLOW}./status_services.sh${NC}"
echo ""
echo -e "${BLUE}🔍 Testy:${NC}"
echo -e "   ${YELLOW}curl http://localhost:$BACKEND_PORT/health${NC}"
echo -e "   ${YELLOW}curl http://localhost:$FRONTEND_PORT/health${NC}"
echo ""

# Opcjonalnie: sprawdź czy usługi odpowiadają
sleep 3
echo -e "${YELLOW}🧪 Szybki test połączenia...${NC}"

if curl -s http://localhost:$BACKEND_PORT/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Backend odpowiada${NC}"
else
    echo -e "${YELLOW}⚠️  Backend jeszcze nie odpowiada (może potrzebować więcej czasu)${NC}"
fi

if curl -s http://localhost:$FRONTEND_PORT/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Frontend odpowiada${NC}"
else
    echo -e "${YELLOW}⚠️  Frontend jeszcze nie odpowiada (może potrzebować więcej czasu)${NC}"
fi

echo ""
echo -e "${GREEN}🎉 Gotowe!${NC}"
