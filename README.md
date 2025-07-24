<div align="center">
  <img src="images/cdnjump-logo 05.png" alt="CDNJump Logo" width="400"/>
  
  # CDN-Jump 🔍
  
  [![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
  [![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
  [![Poetry](https://img.shields.io/badge/Poetry-1.4+-orange.svg)](https://python-poetry.org/)
  
  **CDN-Jump** es una herramienta avanzada de análisis de seguridad diseñada para **detectar posibles bypasses** en servicios de Content Delivery Network (CDN). Combina consultas en tiempo real con análisis históricos para proporcionar una visión completa de la infraestructura de dominios.
</div>

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
- **📝 Sistema de logging avanzado** con archivos separados por dominio

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

### 📝 Sistema de Logging Avanzado

- **Archivos separados por dominio** con timestamp único
- **Formato estructurado** con secciones organizadas
- **Información detallada** de cada etapa del análisis
- **Resumen estadístico** final con métricas
- **Compatibilidad** con análisis individual y múltiples dominios

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
poetry run python -m cdnjump.cli -d ejemplo.com

# Modo interactivo
poetry run python -m cdnjump.cli --interactive

# Analizar múltiples dominios desde archivo
poetry run python -m cdnjump.cli -f dominios.txt

# Modo verbose para más detalles
poetry run python -m cdnjump.cli -d ejemplo.com -v
```

### 📝 Sistema de Logging

Cada análisis genera un archivo de log independiente en la carpeta `results/`:

```bash
# Estructura de archivos generados
results/
├── ejemplo.com_20250724_143021.log
├── google.com_20250724_143025.log
└── github.com_20250724_143030.log
```

**Formato del archivo de log:**
```log
[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO: 
============================================================
           CDN-Jump: Escaneo de ejemplo.com
============================================================
Fecha de inicio: 2025-07-24 14:30:21
Archivo de log: /path/to/results/ejemplo.com_20250724_143021.log
============================================================

[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO: 📡 REGISTROS DNS OBTENIDOS:
[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO:    Dominio: ejemplo.com
[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO:    Registros A: ['192.168.1.1', '192.168.1.2']
[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO:    Total de IPs: 2
[2025-07-24 14:30:21] cdnjump.ejemplo.com - INFO: ----------------------------------------

[2025-07-24 14:30:22] cdnjump.ejemplo.com - INFO: 🔍 RESULTADOS VIRUSTOTAL:
[2025-07-24 14:30:22] cdnjump.ejemplo.com - INFO:    Modo: Básico
[2025-07-24 14:30:22] cdnjump.ejemplo.com - INFO:    IPs históricas: ['192.168.1.1', '192.168.1.2', '10.0.0.1']
[2025-07-24 14:30:22] cdnjump.ejemplo.com - INFO:    Total de IPs: 3
[2025-07-24 14:30:22] cdnjump.ejemplo.com - INFO: ----------------------------------------

[2025-07-24 14:30:23] cdnjump.ejemplo.com - INFO: 🔄 RESULTADOS COMBINADOS:
[2025-07-24 14:30:23] cdnjump.ejemplo.com - INFO:    IPs únicas a validar: ['10.0.0.1', '192.168.1.1', '192.168.1.2']
[2025-07-24 14:30:23] cdnjump.ejemplo.com - INFO:    Total de IPs: 3
[2025-07-24 14:30:23] cdnjump.ejemplo.com - INFO: ----------------------------------------

[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO: 🛡️ RESULTADOS DETECCIÓN CDN:
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    🔄 192.168.1.1: cloudflare
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    🔄 192.168.1.2: cloudflare
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    ✅ 10.0.0.1: Potential CDN bypass
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO: ----------------------------------------

[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO: 📊 RESUMEN DEL ANÁLISIS:
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    Dominio analizado: ejemplo.com
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    Total de IPs analizadas: 3
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    IPs con CDN detectado: 2
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    IPs potencial bypass: 1
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    Archivo de resultados: /path/to/results/ejemplo.com_20250724_143021.log
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO:    Fecha de finalización: 2025-07-24 14:30:24
[2025-07-24 14:30:24] cdnjump.ejemplo.com - INFO: ============================================================
```

### Modos de Escaneo

```bash
# Modo básico (por defecto)
poetry run python -m cdnjump.cli -d ejemplo.com

# Modo intensivo (incluye AS owner)
poetry run python -m cdnjump.cli -d ejemplo.com --intensive

# Modo Censys (búsqueda en certificados)
poetry run python -m cdnjump.cli -d ejemplo.com --censys

# Modo completo (intensivo + Censys)
poetry run python -m cdnjump.cli -d ejemplo.com --intensive --censys
```

### Ejemplos de Uso

```bash
# Análisis básico de un dominio
poetry run python -m cdnjump.cli -d google.com

# Análisis intensivo con verbose
poetry run python -m cdnjump.cli -d github.com --intensive -v

# Procesar lista de dominios
echo "google.com\ngithub.com\nstackoverflow.com" > dominios.txt
poetry run python -m cdnjump.cli -f dominios.txt --censys

# Modo interactivo para explorar opciones
poetry run python -m cdnjump.cli --interactive
```

### 📁 Gestión de Resultados

Los archivos de log se almacenan automáticamente en la carpeta `results/`:

```bash
# Ver archivos de log generados
ls -la results/

# Ver contenido de un log específico
cat results/ejemplo.com_20250724_143021.log

# Buscar logs por dominio
find results/ -name "*google.com*" -type f

# Ver logs recientes
ls -lt results/ | head -10
```

## 📊 Interpretación de Resultados

### Salida Típica

```
[14:30:15] INFO: 📁 Directorio de resultados: /path/to/results
[14:30:15] INFO: 
============================================================
           CDN-Jump: Escaneo de ejemplo.com
============================================================
Fecha de inicio: 2025-07-24 14:30:15
Archivo de log: /path/to/results/ejemplo.com_20250724_143015.log
============================================================

[14:30:15] INFO: 📡 REGISTROS DNS OBTENIDOS:
[14:30:15] INFO:    Dominio: ejemplo.com
[14:30:15] INFO:    Registros A: ['192.168.1.1', '192.168.1.2']
[14:30:15] INFO:    Total de IPs: 2
[14:30:15] INFO: ----------------------------------------

[14:30:16] INFO: 🔍 RESULTADOS VIRUSTOTAL:
[14:30:16] INFO:    Modo: Básico
[14:30:16] INFO:    IPs históricas: ['192.168.1.1', '192.168.1.2', '10.0.0.1']
[14:30:16] INFO:    Total de IPs: 3
[14:30:16] INFO: ----------------------------------------

[14:30:17] INFO: 🔄 RESULTADOS COMBINADOS:
[14:30:17] INFO:    IPs únicas a validar: ['10.0.0.1', '192.168.1.1', '192.168.1.2']
[14:30:17] INFO:    Total de IPs: 3
[14:30:17] INFO: ----------------------------------------

[14:30:18] INFO: 🛡️ RESULTADOS DETECCIÓN CDN:
[14:30:18] INFO:    🔄 192.168.1.1: cloudflare
[14:30:18] INFO:    🔄 192.168.1.2: cloudflare
[14:30:18] INFO:    ✅ 10.0.0.1: Potential CDN bypass
[14:30:18] INFO: ----------------------------------------

[14:30:19] INFO: 📊 RESUMEN DEL ANÁLISIS:
[14:30:19] INFO:    Dominio analizado: ejemplo.com
[14:30:19] INFO:    Total de IPs analizadas: 3
[14:30:19] INFO:    IPs con CDN detectado: 2
[14:30:19] INFO:    IPs potencial bypass: 1
[14:30:19] INFO:    Archivo de resultados: /path/to/results/ejemplo.com_20250724_143015.log
[14:30:19] INFO:    Fecha de finalización: 2025-07-24 14:30:19
[14:30:19] INFO: ============================================================
[14:30:19] INFO: ✅ Análisis completado para ejemplo.com
[14:30:19] INFO: 📄 Log guardado en: /path/to/results/ejemplo.com_20250724_143015.log
```

### Interpretación

- **🔄 `cloudflare`**: IP pertenece a Cloudflare CDN ✅
- **🔄 `akamai`**: IP pertenece a Akamai CDN ✅
- **✅ `Potential CDN bypass`**: ⚠️ **Posible bypass** - IP no identificada como CDN

### 📈 Métricas del Resumen

- **Total de IPs analizadas**: Número total de IPs procesadas
- **IPs con CDN detectado**: IPs identificadas como pertenecientes a CDNs
- **IPs potencial bypass**: IPs que podrían permitir bypass de CDN
- **Archivo de resultados**: Ruta del archivo de log generado

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
│   └── logger.py               # Sistema de logging avanzado
├── config/                     # Configuración
│   └── settings.yaml
├── tests/                      # Tests unitarios
│   ├── test_api.py
│   ├── test_dns.py
│   ├── test_validation.py
│   └── test_cdn.py
├── results/                    # Resultados de análisis (archivos de log)
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

- [x] ✅ Sistema de logging avanzado con archivos separados por dominio
- [ ] Dashboard web para resultados
- [ ] Alertas automáticas por email
- [ ] Integración con más APIs de seguridad
- [ ] Análisis de tendencias temporales
- [ ] Soporte para más proveedores de CDN
- [ ] Exportación a formatos JSON/CSV
- [ ] Compresión y rotación automática de logs

### Mejoras Técnicas

- [ ] Implementación completa de `config.py`
- [ ] Implementación completa de `utils.py`
- [ ] Mejora en gestión de errores
- [ ] Optimización de rendimiento
- [ ] Documentación de API
- [ ] Rate limiting para APIs externas

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

- **Email**: <goalnefesh@protonmail.com>

---

**⚠️ Aviso Legal**: Esta herramienta está diseñada únicamente para auditorías de seguridad autorizadas. Asegúrate de tener permiso antes de analizar cualquier dominio que no sea tuyo.

**🔒 Seguridad**: Nunca compartas tus claves de API en código público. Usa siempre variables de entorno para credenciales sensibles.
