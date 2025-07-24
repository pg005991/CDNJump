# CDN-Jump 🔍

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Poetry](https://img.shields.io/badge/Poetry-1.4+-orange.svg)](https://python-poetry.org/)

**CDN-Jump** es una herramienta avanzada de análisis de seguridad diseñada para **detectar posibles bypasses** en servicios de Content Delivery Network (CDN). Combina consultas en tiempo real con análisis históricos para proporcionar una visión completa de la infraestructura de dominios.

## 🎯 ¿Qué hace CDN-Jump?

CDN-Jump analiza dominios para identificar cuando un atacante puede acceder directamente al servidor de origen, evitando las protecciones de la CDN. Esto es crucial para:

- **🔒 Auditorías de seguridad** - Detectar infraestructura expuesta
- **🛡️ Evaluación de vulnerabilidades** - Identificar bypasses de CDN
- **📊 Análisis de amenazas** - Monitorear cambios en infraestructura
- **⚡ Validación de configuraciones** - Verificar efectividad de protecciones

## ✨ Características Principales

### 🔍 Análisis Integral

- **Consultas DNS** en tiempo real
- **Historial de resoluciones** via VirusTotal API
- **Búsqueda de certificados** via Censys API
- **Validación de contenido** HTTP/HTTPS
- **Detección automática** de CDNs

### 🎛️ Múltiples Modos de Operación

- **Modo Básico**: Escaneo estándar con consultas DNS
- **Modo Intensivo**: Análisis profundo con AS owner y paginación
- **Modo Censys**: Búsqueda avanzada en certificados SSL
- **Modo Todo**: Combinación de todas las técnicas

### 🛠️ Detección de CDNs

Utiliza **tres técnicas** para identificar CDNs:

- **PTR Lookup**: Consulta inversa DNS
- **WHOIS**: Análisis de información de registro
- **Cabeceras HTTP**: Patrones en headers de respuesta

### 📊 CDNs Soportados

- Akamai, Cloudflare, CloudFront
- Fastly, Imperva, KeyCDN
- StackPath, CDN77, BunnyCDN

## 🚀 Instalación

### Prerrequisitos

- Python 3.9 o superior
- Poetry (recomendado) o pip

### Instalación con Poetry (Recomendado)

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/CDNJump.git
cd CDNJump

# Instalar dependencias
poetry install

# Activar el entorno virtual
poetry shell
```

### Instalación con pip

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/CDNJump.git
cd CDNJump

# Instalar dependencias
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Variables de Entorno

El proyecto incluye un archivo `.env-example` como plantilla. Para configurar tu entorno:

```bash
# Copiar la plantilla
cp .env-example .env

# Editar con tus claves de API
nano .env
```

**Contenido del archivo `.env`:**

```bash
# VirusTotal API (obtén tu clave en https://www.virustotal.com/gui/join-us)
VT_API_KEY=tu_virustotal_api_key_aqui

# Censys API (obtén tus credenciales en https://censys.io/register)
CENSYS_API_ID=tu_censys_api_id_aqui
CENSYS_API_SECRET=tu_censys_api_secret_aqui
CENSYS_URL_API=https://search.censys.io
```

**⚠️ Importante:** Nunca subas el archivo `.env` real a GitHub. El `.env-example` sí se puede subir (no contiene claves reales).

### 2. Configuración YAML (Opcional)

Edita `config/settings.yaml` para personalizar:

```yaml
virustotal:
  api_key: "TU_VIRUSTOTAL_API_KEY"

censys:
  api_id: "TU_CENSYS_API_ID"
  api_secret: "TU_CENSYS_API_SECRET"
  domain_api: "api.censys.io"
  url_api: "https://censys.io"

cdns:
  - akamai
  - cloudfront
  - cloudflare
  - fastly
  - imperva
```

## 📖 Uso

### Uso Básico

```bash
# Analizar un dominio único
python -m cdnjump.cli -d ejemplo.com

# Modo interactivo
python -m cdnjump.cli --interactive

# Analizar múltiples dominios desde archivo
python -m cdnjump.cli -f dominios.txt

# Modo verbose para más detalles
python -m cdnjump.cli -d ejemplo.com -v
```

### Modos de Escaneo

```bash
# Modo básico (por defecto)
python -m cdnjump.cli -d ejemplo.com

# Modo intensivo (incluye AS owner)
python -m cdnjump.cli -d ejemplo.com --intensive

# Modo Censys (búsqueda en certificados)
python -m cdnjump.cli -d ejemplo.com --censys

# Modo completo (intensivo + Censys)
python -m cdnjump.cli -d ejemplo.com --intensive --censys
```

### Ejemplos de Uso

```bash
# Análisis básico de un dominio
python -m cdnjump.cli -d google.com

# Análisis intensivo con verbose
python -m cdnjump.cli -d github.com --intensive -v

# Procesar lista de dominios
echo "google.com\ngithub.com\nstackoverflow.com" > dominios.txt
python -m cdnjump.cli -f dominios.txt --censys

# Modo interactivo para explorar opciones
python -m cdnjump.cli --interactive
```

## 📊 Interpretación de Resultados

### Salida Típica

```
[14:30:15] INFO: Iniciando análisis para: ejemplo.com
[14:30:15] INFO: Registros DNS obtenidos: ['192.168.1.1', '192.168.1.2']
[14:30:16] INFO: Modo básico VT: ['192.168.1.1', '192.168.1.2', '10.0.0.1']
[14:30:17] INFO: Resultados Censys: ['10.0.0.2', '10.0.0.3']
[14:30:18] INFO: IP finales a validar: ['10.0.0.1', '10.0.0.2', '10.0.0.3', '192.168.1.1', '192.168.1.2']
[14:30:19] INFO: 192.168.1.1: cloudflare
[14:30:19] INFO: 192.168.1.2: cloudflare
[14:30:20] INFO: 10.0.0.1: Potential CDN bypass
[14:30:20] INFO: 10.0.0.2: akamai
[14:30:20] INFO: 10.0.0.3: Potential CDN bypass
```

### Interpretación

- **`cloudflare`**: IP pertenece a Cloudflare CDN ✅
- **`akamai`**: IP pertenece a Akamai CDN ✅
- **`Potential CDN bypass`**: ⚠️ **Posible bypass** - IP no identificada como CDN

## 🏗️ Estructura del Proyecto

```
CDNJump/
├── cdnjump/                    # Código fuente principal
│   ├── __init__.py
│   ├── main.py                 # Orquestador principal
│   ├── cli.py                  # Interfaz de línea de comandos
│   ├── dns_records.py          # Consultas DNS
│   ├── api/                    # APIs externas
│   │   ├── virustotal.py       # VirusTotal API
│   │   └── censys.py           # Censys API
│   ├── validation.py           # Validación de contenido
│   ├── cdn.py                  # Detección de CDNs
│   └── logger.py               # Sistema de logging
├── config/                     # Configuración
│   └── settings.yaml
├── tests/                      # Tests unitarios
│   ├── test_api.py
│   ├── test_dns.py
│   ├── test_validation.py
│   └── test_cdn.py
├── results/                    # Resultados de análisis
├── scans/                      # Escaneos por dominio
├── pyproject.toml              # Configuración Poetry
└── README.md                   # Este archivo
```

## 🧪 Testing

```bash
# Ejecutar todos los tests
poetry run pytest

# Tests con cobertura
poetry run pytest --cov=cdnjump

# Tests específicos
poetry run pytest tests/test_api.py
poetry run pytest tests/test_cdn.py
```

## 🔧 Desarrollo

### Configuración del Entorno de Desarrollo

```bash
# Clonar y configurar
git clone https://github.com/tu-usuario/CDNJump.git
cd CDNJump

# Instalar dependencias de desarrollo
poetry install

# Instalar pre-commit hooks
poetry run pre-commit install

# Activar entorno virtual
poetry shell
```

### Deployment Automatizado

El proyecto incluye un script de deployment automatizado:

```bash
# Ejecutar deployment automatizado
./deploy.sh
```

**El script realizará:**
- ✅ Verificación de prerrequisitos
- ✅ Validación de archivos críticos
- ✅ Protección de archivos sensibles
- ✅ Limpieza de archivos temporales
- ✅ Configuración de Git
- ✅ Commit inicial profesional
- ✅ Conexión con GitHub
- ✅ Subida del proyecto
- ✅ Creación de tag inicial

**Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas.**

### Estructura de Tests

```bash
tests/
├── test_api.py          # Tests para APIs externas
├── test_dns.py          # Tests para consultas DNS
├── test_validation.py   # Tests para validación
└── test_cdn.py          # Tests para detección CDN
```

## 📈 Roadmap

### Próximas Características

- [ ] Dashboard web para resultados
- [ ] Alertas automáticas por email
- [ ] Integración con más APIs de seguridad
- [ ] Análisis de tendencias temporales
- [ ] Soporte para más proveedores de CDN
- [ ] Exportación a formatos JSON/CSV

### Mejoras Técnicas

- [ ] Implementación completa de `config.py`
- [ ] Implementación completa de `utils.py`
- [ ] Mejora en gestión de errores
- [ ] Optimización de rendimiento
- [ ] Documentación de API

## 🤝 Contribuir

1. **Fork** el proyecto
2. Crea una **rama** para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. Abre un **Pull Request**

### Guías de Contribución

- Sigue las convenciones de código Python (PEP 8)
- Añade tests para nuevas funcionalidades
- Actualiza la documentación según sea necesario
- Verifica que todos los tests pasen antes de hacer PR

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🙏 Agradecimientos

- **VirusTotal** por proporcionar acceso a su API
- **Censys** por su API de búsqueda de certificados
- **dnspython** por la librería de consultas DNS
- **BeautifulSoup** por el parsing de HTML

## 📞 Soporte

- **Issues**: [GitHub Issues](https://github.com/tu-usuario/CDNJump/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tu-usuario/CDNJump/discussions)
- **Email**: <goalnefesh@protonmail.com>

---

**⚠️ Aviso Legal**: Esta herramienta está diseñada únicamente para auditorías de seguridad autorizadas. Asegúrate de tener permiso antes de analizar cualquier dominio que no sea tuyo.

**🔒 Seguridad**: Nunca compartas tus claves de API en código público. Usa siempre variables de entorno para credenciales sensibles.
