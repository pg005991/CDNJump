# 🚀 Guía de Deployment - CDNJump

Esta guía te ayudará a subir el proyecto CDNJump a GitHub de forma segura y profesional.

## 📋 Checklist Pre-Deployment

### ✅ Verificar Archivos Críticos

```bash
# Verificar que estos archivos existen
ls -la
# Deberías ver:
# - README.md
# - pyproject.toml
# - .env-example
# - .gitignore
# - cdnjump/ (directorio)
# - tests/ (directorio)
# - config/ (directorio)
```

### ✅ Verificar que NO hay archivos sensibles

```bash
# Verificar que .env NO existe (o está en .gitignore)
ls -la .env 2>/dev/null || echo "✅ .env no existe (correcto)"

# Verificar contenido de .gitignore
grep -E "\.env|results/|scans/" .gitignore
# Deberías ver estas líneas en .gitignore
```

## 🔧 Configuración Inicial de Git

### 1. Inicializar Repositorio

```bash
# Inicializar git (si no está inicializado)
git init

# Verificar estado
git status
```

### 2. Configurar Git (si es primera vez)

```bash
# Configurar usuario (reemplaza con tus datos)
git config user.name "Tu Nombre"
git config user.email "tu-email@ejemplo.com"

# Verificar configuración
git config --list
```

## 📦 Preparar el Proyecto

### 1. Verificar Estructura

```bash
# Verificar estructura del proyecto
tree -a -I '.git|__pycache__|*.pyc|.pytest_cache|.venv' || find . -type f -name "*.py" -o -name "*.md" -o -name "*.toml" -o -name "*.yaml" -o -name ".env*" -o -name ".gitignore"
```

### 2. Verificar Archivos de Configuración

```bash
# Verificar pyproject.toml
cat pyproject.toml

# Verificar .env-example
head -10 .env-example

# Verificar .gitignore
head -10 .gitignore
```

### 3. Limpiar Archivos Temporales

```bash
# Eliminar archivos Python compilados
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

# Eliminar archivos de pytest cache
rm -rf .pytest_cache/

# Verificar que no hay archivos sensibles
find . -name ".env" -o -name "*.key" -o -name "*.pem"
```

## 🎯 Crear Repositorio en GitHub

### 1. Crear Repositorio

1. Ve a [GitHub](https://github.com)
2. Haz clic en **"New repository"**
3. Configura el repositorio:
   - **Repository name**: `CDNJump`
   - **Description**: `Herramienta avanzada para detectar bypasses de CDN`
   - **Visibility**: Public (o Private si prefieres)
   - **NO** marques "Add a README file" (ya tenemos uno)
   - **NO** marques "Add .gitignore" (ya tenemos uno)
   - **NO** marques "Choose a license" (ya tenemos MIT)

### 2. Copiar URL del Repositorio

```bash
# Reemplaza con tu URL real
GITHUB_URL="https://github.com/tu-usuario/CDNJump.git"
```

## 📤 Subir a GitHub

### 1. Añadir Archivos

```bash
# Ver qué archivos se van a añadir
git status

# Añadir todos los archivos (excepto los ignorados)
git add .

# Verificar qué se va a commitear
git status
```

### 2. Primer Commit

```bash
# Commit inicial
git commit -m "🎉 Initial commit: CDNJump - CDN bypass detection tool

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
```

### 3. Conectar con GitHub

```bash
# Añadir remote (reemplaza con tu URL)
git remote add origin https://github.com/tu-usuario/CDNJump.git

# Verificar remote
git remote -v
```

### 4. Subir a GitHub

```bash
# Subir a la rama main
git push -u origin main

# Verificar que se subió correctamente
git status
```

## 🔍 Verificación Post-Deployment

### 1. Verificar en GitHub

1. Ve a tu repositorio en GitHub
2. Verifica que **NO** aparece el archivo `.env`
3. Verifica que **SÍ** aparece `.env-example`
4. Verifica que **SÍ** aparece `.gitignore`
5. Verifica que **SÍ** aparece `README.md`

### 2. Verificar Estructura

```bash
# Clonar en un directorio temporal para verificar
cd /tmp
git clone https://github.com/tu-usuario/CDNJump.git CDNJump-test
cd CDNJump-test

# Verificar estructura
ls -la

# Verificar que NO hay archivos sensibles
find . -name ".env" -o -name "*.key" -o -name "*.pem"

# Limpiar
cd ..
rm -rf CDNJump-test
```

## 🏷️ Crear Release Inicial

### 1. Crear Tag

```bash
# Crear tag para la versión inicial
git tag -a v0.1.0 -m "🎉 Initial release: CDNJump v0.1.0

✨ Features:
- Complete CDN bypass detection tool
- Multiple API integrations
- Comprehensive testing suite
- Professional documentation

🔧 Technical:
- Python 3.9+ support
- Poetry dependency management
- Security-focused design"

# Subir tag
git push origin v0.1.0
```

### 2. Crear Release en GitHub

1. Ve a tu repositorio en GitHub
2. Haz clic en **"Releases"**
3. Haz clic en **"Create a new release"**
4. Selecciona el tag `v0.1.0`
5. Título: `🎉 Initial Release: CDNJump v0.1.0`
6. Descripción: Copia el contenido del commit inicial

## 🔧 Configuración Adicional

### 1. Configurar GitHub Pages (Opcional)

```bash
# Crear rama gh-pages
git checkout -b gh-pages

# Crear documentación básica
mkdir docs
echo "# CDNJump Documentation" > docs/index.md

# Commit y push
git add docs/
git commit -m "📚 Add documentation structure"
git push origin gh-pages

# Volver a main
git checkout main
```

### 2. Configurar GitHub Actions (Opcional)

Crear `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.9, 3.10, 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install poetry
        poetry install
    - name: Run tests
      run: |
        poetry run pytest
```

## 📊 Métricas de Éxito

### ✅ Checklist Final

- [ ] Repositorio creado en GitHub
- [ ] Todos los archivos subidos correctamente
- [ ] `.env` NO está en el repositorio
- [ ] `.env-example` SÍ está en el repositorio
- [ ] README.md se ve correctamente
- [ ] Tests pasan localmente
- [ ] Tag v0.1.0 creado
- [ ] Release publicado
- [ ] Documentación completa

### 📈 Próximos Pasos

1. **Configurar Issues**: Crear templates para bugs y features
2. **Configurar Discussions**: Habilitar para comunidad
3. **Configurar Security**: Habilitar security advisories
4. **Configurar Dependabot**: Para actualizaciones automáticas
5. **Configurar CodeQL**: Para análisis de seguridad

## 🆘 Troubleshooting

### Problema: "Permission denied"
```bash
# Configurar SSH o usar HTTPS con token
git remote set-url origin https://tu-token@github.com/tu-usuario/CDNJump.git
```

### Problema: ".env se subió por accidente"
```bash
# Eliminar del repositorio (mantiene local)
git rm --cached .env
git commit -m "🔒 Remove .env file from repository"
git push origin main
```

### Problema: "Archivos grandes no se suben"
```bash
# Verificar archivos grandes
find . -size +50M

# Añadir a .gitignore si es necesario
echo "archivo_grande.zip" >> .gitignore
```

## 🎉 ¡Listo!

Tu proyecto CDNJump está ahora en GitHub de forma segura y profesional. 

**Recuerda:**
- Nunca subas archivos `.env` con claves reales
- Mantén actualizada la documentación
- Responde a issues y pull requests
- Actualiza regularmente las dependencias

¡Feliz coding! 🚀 