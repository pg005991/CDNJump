---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: ['bug', 'triage']
assignees: ['goalnefesh']

---

## 🐛 Descripción del Bug

Una descripción clara y concisa del bug.

## 🔄 Pasos para Reproducir

1. Ir a '...'
2. Hacer clic en '....'
3. Desplazarse hacia abajo hasta '....'
4. Ver error

## ✅ Comportamiento Esperado

Una descripción clara de lo que esperabas que sucediera.

## 📸 Capturas de Pantalla

Si es aplicable, añade capturas de pantalla para ayudar a explicar tu problema.

## 🖥️ Información del Sistema

**Sistema Operativo:**
- [ ] Windows
- [ ] macOS
- [ ] Linux (especifica distribución)

**Versión de Python:**
```
python --version
```

**Versión de CDNJump:**
```
python -m cdnjump.cli --version
```

## 📋 Configuración

**Archivo .env (sin claves reales):**
```bash
# VirusTotal API
VT_API_KEY=tu_clave_aqui

# Censys API
CENSYS_API_ID=tu_id_aqui
CENSYS_API_SECRET=tu_secret_aqui
CENSYS_URL_API=https://search.censys.io
```

## 📝 Logs

**Comando ejecutado:**
```bash
python -m cdnjump.cli -d ejemplo.com -v
```

**Salida completa:**
```
[Pega aquí la salida completa del comando]
```

## 🔍 Información Adicional

Cualquier otra información sobre el problema aquí.

## ✅ Checklist

- [ ] He verificado que el bug no ha sido reportado anteriormente
- [ ] He incluido todos los pasos para reproducir el bug
- [ ] He incluido información del sistema
- [ ] He incluido logs relevantes
- [ ] He verificado que no es un problema de configuración 