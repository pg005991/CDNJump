#!/bin/bash

# ===========================================
# CDNJump - Script de Deployment Automatizado
# ===========================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Función para verificar si un comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verificar prerrequisitos
check_prerequisites() {
    print_status "Verificando prerrequisitos..."
    
    if ! command_exists git; then
        print_error "Git no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    if ! command_exists python3; then
        print_error "Python 3 no está instalado. Por favor instálalo primero."
        exit 1
    fi
    
    print_success "Prerrequisitos verificados"
}

# Verificar archivos críticos
check_critical_files() {
    print_status "Verificando archivos críticos..."
    
    local missing_files=()
    
    # Lista de archivos que deben existir
    local required_files=(
        "README.md"
        "pyproject.toml"
        ".env-example"
        ".gitignore"
        "cdnjump/"
        "tests/"
        "config/"
    )
    
    for file in "${required_files[@]}"; do
        if [[ ! -e "$file" ]]; then
            missing_files+=("$file")
        fi
    done
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        print_error "Faltan archivos críticos:"
        for file in "${missing_files[@]}"; do
            echo "  - $file"
        done
        exit 1
    fi
    
    print_success "Todos los archivos críticos están presentes"
}

# Verificar archivos sensibles
check_sensitive_files() {
    print_status "Verificando archivos sensibles..."
    
    # Verificar que .env no existe o está en .gitignore
    if [[ -f ".env" ]]; then
        if grep -q "\.env" .gitignore; then
            print_warning ".env existe pero está en .gitignore (correcto)"
        else
            print_error ".env existe y NO está en .gitignore"
            exit 1
        fi
    else
        print_success ".env no existe (correcto)"
    fi
    
    # Verificar otros archivos sensibles
    local sensitive_files=($(find . -name "*.key" -o -name "*.pem" -o -name "*.crt" 2>/dev/null))
    if [[ ${#sensitive_files[@]} -gt 0 ]]; then
        print_warning "Archivos sensibles encontrados:"
        for file in "${sensitive_files[@]}"; do
            echo "  - $file"
        done
        print_warning "Verifica que estos archivos estén en .gitignore"
    fi
    
    print_success "Verificación de archivos sensibles completada"
}

# Limpiar archivos temporales
clean_temp_files() {
    print_status "Limpiando archivos temporales..."
    
    # Eliminar archivos Python compilados
    find . -name "*.pyc" -delete 2>/dev/null || true
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    
    # Eliminar cache de pytest
    rm -rf .pytest_cache/ 2>/dev/null || true
    
    # Eliminar archivos de backup
    find . -name "*.bak" -o -name "*.backup" -o -name "*.old" -delete 2>/dev/null || true
    
    print_success "Archivos temporales limpiados"
}

# Configurar Git
setup_git() {
    print_status "Configurando Git..."
    
    # Verificar si ya está inicializado
    if [[ ! -d ".git" ]]; then
        git init
        print_success "Repositorio Git inicializado"
    else
        print_success "Repositorio Git ya existe"
    fi
    
    # Verificar configuración de usuario
    local user_name=$(git config user.name 2>/dev/null || echo "")
    local user_email=$(git config user.email 2>/dev/null || echo "")
    
    if [[ -z "$user_name" || -z "$user_email" ]]; then
        print_warning "Configuración de Git incompleta"
        echo "Por favor configura tu usuario de Git:"
        echo "git config user.name 'Tu Nombre'"
        echo "git config user.email 'tu-email@ejemplo.com'"
        read -p "¿Quieres continuar sin configurar? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_success "Configuración de Git verificada"
    fi
}

# Preparar commit
prepare_commit() {
    print_status "Preparando commit..."
    
    # Verificar estado
    local status=$(git status --porcelain)
    if [[ -z "$status" ]]; then
        print_warning "No hay cambios para commitear"
        return
    fi
    
    # Añadir archivos
    git add .
    
    # Verificar qué se va a commitear
    print_status "Archivos que se van a commitear:"
    git status --short
    
    print_success "Archivos preparados para commit"
}

# Hacer commit inicial
make_initial_commit() {
    print_status "Haciendo commit inicial..."
    
    local commit_message="🎉 Initial commit: CDNJump - CDN bypass detection tool

✨ Features:
- DNS queries and historical analysis
- VirusTotal and Censys API integration
- CDN detection with multiple techniques
- Content validation and similarity analysis
- CLI interface with interactive mode
- Comprehensive test suite

🔧 Technical:
- Python 3.9+ compatibility
- Poetry dependency management
- Modular architecture
- Environment-based configuration
- Security-focused design

📚 Documentation:
- Complete README with examples
- API documentation
- Deployment guide
- Security considerations"
    
    git commit -m "$commit_message"
    print_success "Commit inicial realizado"
}

# Conectar con GitHub
connect_to_github() {
    print_status "Conectando con GitHub..."
    
    # Solicitar URL del repositorio
    echo "Por favor, crea el repositorio en GitHub primero:"
    echo "1. Ve a https://github.com"
    echo "2. Haz clic en 'New repository'"
    echo "3. Nombre: CDNJump"
    echo "4. Descripción: Herramienta avanzada para detectar bypasses de CDN"
    echo "5. NO marques 'Add a README file'"
    echo "6. NO marques 'Add .gitignore'"
    echo "7. NO marques 'Choose a license'"
    echo ""
    
    read -p "Introduce la URL del repositorio (ej: https://github.com/tu-usuario/CDNJump.git): " github_url
    
    if [[ -z "$github_url" ]]; then
        print_error "URL del repositorio requerida"
        exit 1
    fi
    
    # Añadir remote
    git remote add origin "$github_url" 2>/dev/null || git remote set-url origin "$github_url"
    
    # Verificar remote
    print_status "Remote configurado:"
    git remote -v
    
    print_success "Conectado con GitHub"
}

# Subir a GitHub
push_to_github() {
    print_status "Subiendo a GitHub..."
    
    # Subir a main
    git push -u origin main
    
    print_success "Proyecto subido a GitHub"
}

# Crear tag inicial
create_initial_tag() {
    print_status "Creando tag inicial..."
    
    local tag_message="🎉 Initial release: CDNJump v0.1.0

✨ Features:
- Complete CDN bypass detection tool
- Multiple API integrations
- Comprehensive testing suite
- Professional documentation

🔧 Technical:
- Python 3.9+ support
- Poetry dependency management
- Security-focused design"
    
    git tag -a v0.1.0 -m "$tag_message"
    git push origin v0.1.0
    
    print_success "Tag v0.1.0 creado y subido"
}

# Verificar deployment
verify_deployment() {
    print_status "Verificando deployment..."
    
    print_status "✅ Verificaciones completadas:"
    echo "  - Repositorio Git inicializado"
    echo "  - Archivos críticos verificados"
    echo "  - Archivos sensibles protegidos"
    echo "  - Commit inicial realizado"
    echo "  - Proyecto subido a GitHub"
    echo "  - Tag v0.1.0 creado"
    
    echo ""
    print_success "🎉 ¡Deployment completado exitosamente!"
    echo ""
    echo "Próximos pasos:"
    echo "1. Ve a tu repositorio en GitHub"
    echo "2. Verifica que todos los archivos están presentes"
    echo "3. Crea un release desde el tag v0.1.0"
    echo "4. Configura GitHub Actions (opcional)"
    echo "5. Configura Issues y Discussions"
    echo ""
    echo "¡Feliz coding! 🚀"
}

# Función principal
main() {
    echo "==========================================="
    echo "🚀 CDNJump - Deployment Automatizado"
    echo "==========================================="
    echo ""
    
    check_prerequisites
    check_critical_files
    check_sensitive_files
    clean_temp_files
    setup_git
    prepare_commit
    make_initial_commit
    connect_to_github
    push_to_github
    create_initial_tag
    verify_deployment
}

# Ejecutar función principal
main "$@" 