#!/bin/bash
# =============================================================================
# BulkDeal Analyzer - Development Server Runner
# =============================================================================
# Starts both backend (FastAPI) and frontend (Next.js) servers.
#
# Usage:
#   ./scripts/run_dev.sh          # Start both servers
#   ./scripts/run_dev.sh backend  # Start backend only
#   ./scripts/run_dev.sh frontend # Start frontend only
#   ./scripts/run_dev.sh stop     # Stop all running servers
#   ./scripts/run_dev.sh status   # Check server status
#   ./scripts/run_dev.sh test     # Run all tests then start servers
# =============================================================================

set -e

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
PID_DIR="$ROOT_DIR/.pids"
LOG_DIR="$ROOT_DIR/.logs"

BACKEND_PORT=8000
FRONTEND_PORT=3000

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# -----------------------------------------------------------------------------
# Helpers
# -----------------------------------------------------------------------------

log_info()  { echo -e "${BLUE}[INFO]${NC}  $1"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $1"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step()  { echo -e "${CYAN}[STEP]${NC}  $1"; }

banner() {
    echo ""
    echo -e "${BOLD}${CYAN}======================================${NC}"
    echo -e "${BOLD}${CYAN}  BulkDeal Analyzer - Dev Server${NC}"
    echo -e "${BOLD}${CYAN}======================================${NC}"
    echo ""
}

ensure_dirs() {
    mkdir -p "$PID_DIR" "$LOG_DIR"
}

# -----------------------------------------------------------------------------
# Port & Process management
# -----------------------------------------------------------------------------

is_port_in_use() {
    local port=$1
    # Try ss first (most reliable on Linux)
    if command -v ss &> /dev/null; then
        ss -tlnH "sport = :$port" 2>/dev/null | grep -q "$port"
        return $?
    fi
    if command -v lsof &> /dev/null; then
        lsof -i :"$port" -sTCP:LISTEN -t &> /dev/null
        return $?
    fi
    netstat -tlnp 2>/dev/null | grep -q ":$port "
}

get_pid_on_port() {
    local port=$1
    if command -v lsof &> /dev/null; then
        lsof -i :"$port" -sTCP:LISTEN -t 2>/dev/null | head -1
    fi
}

kill_port() {
    local port=$1
    local name=$2

    # Kill all processes listening on the port
    if command -v fuser &> /dev/null; then
        fuser -k "$port/tcp" 2>/dev/null || true
    fi

    local pid
    pid=$(get_pid_on_port "$port")
    if [ -n "$pid" ]; then
        log_warn "Stopping $name (PID $pid) on port $port"
        kill "$pid" 2>/dev/null || true
        sleep 1
        # Force kill if still running
        if kill -0 "$pid" 2>/dev/null; then
            kill -9 "$pid" 2>/dev/null || true
        fi
    fi

    sleep 1
}

save_pid() {
    local name=$1
    local pid=$2
    echo "$pid" > "$PID_DIR/$name.pid"
}

read_pid() {
    local name=$1
    local pidfile="$PID_DIR/$name.pid"
    if [ -f "$pidfile" ]; then
        cat "$pidfile"
    fi
}

# -----------------------------------------------------------------------------
# Environment checks
# -----------------------------------------------------------------------------

check_prerequisites() {
    log_step "Checking prerequisites..."

    # Python
    if ! command -v python3 &> /dev/null; then
        log_error "python3 not found. Install Python 3.10+"
        exit 1
    fi
    log_ok "Python: $(python3 --version 2>&1)"

    # Node
    if ! command -v node &> /dev/null; then
        log_error "node not found. Install Node.js 18+"
        exit 1
    fi
    log_ok "Node:   $(node --version)"

    # npm
    if ! command -v npm &> /dev/null; then
        log_error "npm not found. Install npm"
        exit 1
    fi
    log_ok "npm:    $(npm --version)"

    echo ""
}

check_env_files() {
    log_step "Checking environment files..."

    if [ ! -f "$BACKEND_DIR/.env" ]; then
        log_warn "backend/.env not found - using defaults (auth won't work with real Supabase)"
    else
        log_ok "backend/.env exists"
    fi

    if [ ! -f "$FRONTEND_DIR/.env.local" ]; then
        log_warn "frontend/.env.local not found - copying from env.example"
        if [ -f "$FRONTEND_DIR/env.example" ]; then
            cp "$FRONTEND_DIR/env.example" "$FRONTEND_DIR/.env.local"
            log_warn "Please edit frontend/.env.local with your Supabase credentials"
        fi
    else
        log_ok "frontend/.env.local exists"
    fi

    echo ""
}

# -----------------------------------------------------------------------------
# Install dependencies
# -----------------------------------------------------------------------------

install_backend_deps() {
    log_step "Installing backend dependencies..."
    if [ -f "$BACKEND_DIR/requirements.txt" ]; then
        pip3 install -q -r "$BACKEND_DIR/requirements.txt" 2>&1 | tail -1
        log_ok "Backend dependencies installed"
    else
        log_warn "No requirements.txt found"
    fi
}

install_frontend_deps() {
    log_step "Installing frontend dependencies..."
    if [ -f "$FRONTEND_DIR/package.json" ]; then
        if [ ! -d "$FRONTEND_DIR/node_modules" ]; then
            (cd "$FRONTEND_DIR" && npm install --silent 2>&1 | tail -1)
            log_ok "Frontend dependencies installed"
        else
            log_ok "Frontend node_modules exists (skipping install)"
        fi
    else
        log_warn "No package.json found"
    fi
}

# -----------------------------------------------------------------------------
# Start servers
# -----------------------------------------------------------------------------

start_backend() {
    log_step "Starting backend (FastAPI) on port $BACKEND_PORT..."

    if is_port_in_use "$BACKEND_PORT"; then
        log_warn "Port $BACKEND_PORT already in use"
        local existing_pid
        existing_pid=$(get_pid_on_port "$BACKEND_PORT")
        log_warn "Existing process PID: $existing_pid"
        echo -n "  Kill and restart? [y/N] "
        read -r answer
        if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
            kill_port "$BACKEND_PORT" "backend"
        else
            log_info "Keeping existing backend"
            return 0
        fi
    fi

    (cd "$BACKEND_DIR" && python3 -m uvicorn app.main:app \
        --reload \
        --host 0.0.0.0 \
        --port "$BACKEND_PORT" \
        > "$LOG_DIR/backend.log" 2>&1) &

    local pid=$!
    save_pid "backend" "$pid"

    # Wait for startup
    local tries=0
    while [ $tries -lt 15 ]; do
        if is_port_in_use "$BACKEND_PORT"; then
            log_ok "Backend running  -> http://localhost:$BACKEND_PORT"
            log_ok "API Docs         -> http://localhost:$BACKEND_PORT/docs"
            return 0
        fi
        sleep 1
        tries=$((tries + 1))
    done

    log_error "Backend failed to start. Check $LOG_DIR/backend.log"
    return 1
}

start_frontend() {
    log_step "Starting frontend (Next.js) on port $FRONTEND_PORT..."

    if is_port_in_use "$FRONTEND_PORT"; then
        log_warn "Port $FRONTEND_PORT already in use"
        local existing_pid
        existing_pid=$(get_pid_on_port "$FRONTEND_PORT")
        log_warn "Existing process PID: $existing_pid"
        echo -n "  Kill and restart? [y/N] "
        read -r answer
        if [ "$answer" = "y" ] || [ "$answer" = "Y" ]; then
            kill_port "$FRONTEND_PORT" "frontend"
            sleep 1
        else
            log_info "Keeping existing frontend"
            return 0
        fi
    fi

    # Remove stale Next.js lock file
    rm -f "$FRONTEND_DIR/.next/dev/lock"

    (cd "$FRONTEND_DIR" && npm run dev -- --port "$FRONTEND_PORT" \
        > "$LOG_DIR/frontend.log" 2>&1) &

    local pid=$!
    save_pid "frontend" "$pid"

    # Wait for startup (Next.js can be slow on first compile)
    local tries=0
    while [ $tries -lt 40 ]; do
        if is_port_in_use "$FRONTEND_PORT"; then
            log_ok "Frontend running -> http://localhost:$FRONTEND_PORT"
            return 0
        fi
        sleep 1
        tries=$((tries + 1))
    done

    log_error "Frontend failed to start. Check $LOG_DIR/frontend.log"
    return 1
}

# -----------------------------------------------------------------------------
# Stop servers
# -----------------------------------------------------------------------------

stop_all() {
    log_step "Stopping all servers..."

    kill_port "$BACKEND_PORT" "backend"
    kill_port "$FRONTEND_PORT" "frontend"

    # Clean up PID files
    rm -f "$PID_DIR/backend.pid" "$PID_DIR/frontend.pid"

    log_ok "All servers stopped"
}

# -----------------------------------------------------------------------------
# Status
# -----------------------------------------------------------------------------

show_status() {
    echo ""
    echo -e "${BOLD}Service Status:${NC}"
    echo "─────────────────────────────────────────"

    if is_port_in_use "$BACKEND_PORT"; then
        local bpid
        bpid=$(get_pid_on_port "$BACKEND_PORT")
        echo -e "  Backend  (:$BACKEND_PORT)  ${GREEN}RUNNING${NC}  PID: $bpid"
    else
        echo -e "  Backend  (:$BACKEND_PORT)  ${RED}STOPPED${NC}"
    fi

    if is_port_in_use "$FRONTEND_PORT"; then
        local fpid
        fpid=$(get_pid_on_port "$FRONTEND_PORT")
        echo -e "  Frontend (:$FRONTEND_PORT)  ${GREEN}RUNNING${NC}  PID: $fpid"
    else
        echo -e "  Frontend (:$FRONTEND_PORT)  ${RED}STOPPED${NC}"
    fi

    echo "─────────────────────────────────────────"
    echo ""
}

# -----------------------------------------------------------------------------
# Run tests
# -----------------------------------------------------------------------------

run_tests() {
    log_step "Running backend tests..."
    (cd "$BACKEND_DIR" && python3 -m pytest tests/ -v --tb=short)
    echo ""
    log_step "Running backend lint..."
    (cd "$BACKEND_DIR" && ruff check .)
    echo ""
    log_ok "All checks passed!"
    echo ""
}

# -----------------------------------------------------------------------------
# Summary
# -----------------------------------------------------------------------------

show_summary() {
    echo ""
    echo -e "${BOLD}${GREEN}All services started successfully!${NC}"
    echo ""
    echo "─────────────────────────────────────────────────"
    echo -e "  ${BOLD}Frontend${NC}   http://localhost:$FRONTEND_PORT"
    echo -e "  ${BOLD}Backend${NC}    http://localhost:$BACKEND_PORT"
    echo -e "  ${BOLD}API Docs${NC}   http://localhost:$BACKEND_PORT/docs"
    echo -e "  ${BOLD}API Health${NC} http://localhost:$BACKEND_PORT/api/v1/health/"
    echo "─────────────────────────────────────────────────"
    echo ""
    echo -e "  Logs:   ${CYAN}$LOG_DIR/${NC}"
    echo -e "  Stop:   ${CYAN}./scripts/run_dev.sh stop${NC}"
    echo -e "  Status: ${CYAN}./scripts/run_dev.sh status${NC}"
    echo ""
}

# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------

main() {
    local mode="${1:-all}"

    case "$mode" in
        stop)
            ensure_dirs
            stop_all
            ;;
        status)
            show_status
            ;;
        test)
            banner
            run_tests
            ensure_dirs
            check_prerequisites
            check_env_files
            start_backend
            start_frontend
            show_summary
            ;;
        backend)
            banner
            ensure_dirs
            check_prerequisites
            check_env_files
            install_backend_deps
            start_backend
            show_status
            ;;
        frontend)
            banner
            ensure_dirs
            check_prerequisites
            check_env_files
            install_frontend_deps
            start_frontend
            show_status
            ;;
        all|"")
            banner
            ensure_dirs
            check_prerequisites
            check_env_files
            install_backend_deps
            install_frontend_deps
            echo ""
            start_backend
            start_frontend
            show_summary
            ;;
        *)
            echo "Usage: $0 {all|backend|frontend|stop|status|test}"
            echo ""
            echo "Commands:"
            echo "  all       Start both backend and frontend (default)"
            echo "  backend   Start backend only"
            echo "  frontend  Start frontend only"
            echo "  stop      Stop all running servers"
            echo "  status    Show server status"
            echo "  test      Run tests then start servers"
            exit 1
            ;;
    esac
}

main "$@"
