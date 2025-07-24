# 🤝 Guía de Contribución - CDNJump

¡Gracias por tu interés en contribuir a CDNJump! Este documento te ayudará a entender cómo puedes contribuir al proyecto.

## 📋 Tabla de Contenidos

- [Código de Conducta](#código-de-conducta)
- [Cómo Contribuir](#cómo-contribuir)
- [Configuración del Entorno](#configuración-del-entorno)
- [Guías de Desarrollo](#guías-de-desarrollo)
- [Tests](#tests)
- [Documentación](#documentación)
- [Releases](#releases)

## 📜 Código de Conducta

Este proyecto y sus participantes se rigen por el [Código de Conducta de Contribuidores](CODE_OF_CONDUCT.md). Al participar, se espera que respetes este código.

## 🚀 Cómo Contribuir

### Reportar Bugs

1. **Busca issues existentes**: Antes de crear un nuevo issue, busca si ya existe uno similar.
2. **Usa la plantilla**: Utiliza la plantilla de bug report para proporcionar toda la información necesaria.
3. **Incluye logs**: Siempre incluye logs completos y pasos para reproducir el bug.

### Solicitar Características

1. **Describe claramente**: Explica qué característica necesitas y por qué es útil.
2. **Considera alternativas**: Investiga si ya existe una solución similar.
3. **Proporciona contexto**: Incluye casos de uso específicos y ejemplos.

### Contribuir Código

1. **Fork el repositorio**: Crea tu propio fork del proyecto.
2. **Crea una rama**: Crea una rama para tu feature o fix.
3. **Desarrolla**: Implementa tus cambios siguiendo las guías.
4. **Tests**: Asegúrate de que todos los tests pasen.
5. **Documenta**: Actualiza la documentación según sea necesario.
6. **Pull Request**: Crea un PR con una descripción clara.

## 🔧 Configuración del Entorno

### Prerrequisitos

- Python 3.9+
- Poetry
- Git

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/CDNJump.git
cd CDNJump

# Instalar dependencias
poetry install

# Activar entorno virtual
poetry shell

# Configurar variables de entorno
cp .env-example .env
# Editar .env con tus claves de API
```

### Configuración de Desarrollo

```bash
# Instalar dependencias de desarrollo
poetry install --with dev

# Configurar pre-commit hooks
poetry run pre-commit install

# Verificar configuración
poetry run pytest
```

## 📝 Guías de Desarrollo

### Estilo de Código

- **PEP 8**: Sigue las convenciones de PEP 8
- **Black**: Usa Black para formateo automático
- **Flake8**: Usa Flake8 para linting
- **Docstrings**: Documenta todas las funciones públicas

### Estructura de Commits

Usa el formato de commits convencionales:

```
tipo(alcance): descripción

[body opcional]

[footer opcional]
```

**Tipos:**
- `feat`: Nueva característica
- `fix`: Corrección de bug
- `docs`: Documentación
- `style`: Formato, punto y coma, etc.
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Tareas de mantenimiento

**Ejemplos:**
```
feat(api): añadir soporte para nueva API de Censys
fix(dns): corregir timeout en consultas DNS
docs(readme): actualizar ejemplos de uso
```

### Estructura de Ramas

- `main`: Rama principal, código estable
- `develop`: Rama de desarrollo
- `feature/nombre-caracteristica`: Nuevas características
- `fix/nombre-bug`: Correcciones de bugs
- `docs/nombre-documentacion`: Cambios en documentación

## 🧪 Tests

### Ejecutar Tests

```bash
# Todos los tests
poetry run pytest

# Tests específicos
poetry run pytest tests/test_api.py

# Tests con cobertura
poetry run pytest --cov=cdnjump

# Tests con verbose
poetry run pytest -v
```

### Escribir Tests

- **Naming**: Usa nombres descriptivos para los tests
- **Independencia**: Cada test debe ser independiente
- **Mocks**: Usa mocks para APIs externas
- **Cobertura**: Mantén alta cobertura de código

**Ejemplo:**
```python
def test_get_dns_a_records_success():
    """Test successful DNS A record retrieval."""
    result = get_dns_a_records("example.com")
    assert isinstance(result, list)
    assert all(isinstance(ip, str) for ip in result)
```

## 📚 Documentación

### Documentación de Código

- **Docstrings**: Usa docstrings para todas las funciones públicas
- **Type hints**: Incluye type hints en todas las funciones
- **Ejemplos**: Proporciona ejemplos de uso

**Ejemplo:**
```python
def get_dns_a_records(domain: str, resolver: str = "1.1.1.1") -> list[str]:
    """
    Realiza una consulta DNS para obtener los registros A del dominio.
    
    Args:
        domain: El dominio a consultar
        resolver: Servidor DNS a utilizar
        
    Returns:
        Lista de direcciones IP asociadas al dominio
        
    Raises:
        Exception: Si la consulta DNS falla
    """
```

### Documentación del Proyecto

- **README.md**: Mantén actualizado el README principal
- **API docs**: Documenta la API pública
- **Ejemplos**: Proporciona ejemplos de uso
- **Changelog**: Mantén un registro de cambios

## 🏷️ Releases

### Proceso de Release

1. **Desarrollo**: Desarrolla en rama `develop`
2. **Testing**: Asegúrate de que todos los tests pasen
3. **Merge**: Mergea `develop` a `main`
4. **Tag**: Crea un tag con la nueva versión
5. **Release**: Crea un release en GitHub

### Versionado

Usa [Semantic Versioning](https://semver.org/):

- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas características compatibles
- **PATCH**: Correcciones de bugs compatibles

### Crear Release

```bash
# Actualizar versión en pyproject.toml
# Crear tag
git tag -a v1.0.0 -m "Release v1.0.0"

# Subir tag
git push origin v1.0.0

# Crear release en GitHub
```

## 🔍 Review Process

### Antes de Crear un PR

- [ ] Código sigue las guías de estilo
- [ ] Tests pasan localmente
- [ ] Documentación actualizada
- [ ] Commits siguen convenciones
- [ ] No hay conflictos con main

### Durante el Review

- **Responde a feedback**: Responde a todos los comentarios
- **Actualiza según sea necesario**: Haz cambios basados en feedback
- **Mantén conversación**: Comunícate claramente con reviewers

### Después del Merge

- **Limpia ramas**: Elimina ramas feature después del merge
- **Actualiza documentación**: Asegúrate de que la documentación esté actualizada
- **Celebra**: ¡Celebra tu contribución!

## 🆘 Obtener Ayuda

### Canales de Comunicación

- **Issues**: Para bugs y solicitudes de características
- **Discussions**: Para preguntas generales
- **Email**: goalnefesh@protonmail.com

### Recursos Útiles

- [Documentación de Python](https://docs.python.org/)
- [Guía de PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Documentación de Poetry](https://python-poetry.org/docs/)
- [Guía de Git](https://git-scm.com/doc)

## 🙏 Reconocimientos

Gracias a todos los contribuidores que han ayudado a hacer CDNJump mejor:

- [Lista de contribuidores](https://github.com/tu-usuario/CDNJump/graphs/contributors)

---

**¿Tienes preguntas?** No dudes en abrir un issue o contactar directamente.

¡Gracias por contribuir a CDNJump! 🚀 