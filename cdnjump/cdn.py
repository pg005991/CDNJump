"""
Módulo cdn_validation.py para CDN-Jump

Este módulo implementa la detección de CDNs utilizando tres técnicas:
  1. Búsqueda PTR: Se realiza una consulta inversa para obtener el hostname asociado a una IP.
  2. Consulta WHOIS: Se ejecuta una consulta whois para extraer información de registro.
  3. Inspección de cabeceras HTTP: Se realiza una petición HTTP forzando la resolución
     a la IP indicada y se analizan las cabeceras para detectar patrones propios de CDNs.

Si ninguna de estas técnicas detecta un CDN, se considera que la IP podría ser un bypass.
"""
import logging
import re
import socket
import subprocess
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Diccionario con palabras clave de CDNs conocidos.
CDN_KEYWORDS = {
    "akamai": ["akamai"],
    "cloudflare": ["cloudflare", "cf-"],
    "fastly": ["fastly"],
    "cloudfront": ["cloudfront"],
    "imperva": ["imperva", "incapsula"],
    "keycdn": ["keycdn"],
    "stackpath": ["stackpath"],
    "cdn77": ["cdn77"],
    "bunnycdn": ["bunnycdn"],
    # Se pueden añadir más patrones.
}

def cdn_validation_by_PTR_register(ip: str) -> str:
    """
    Realiza una consulta PTR para obtener el hostname asociado a la IP y verifica
    si el hostname contiene alguna palabra clave de un CDN.
    
    Nota: En una implementación real se podría utilizar un paquete especializado o
    personalizar el timeout y la gestión de errores.
    """
    try:
        hostname, _, _ = socket.gethostbyaddr(ip)
        logger.debug(f"PTR lookup de {ip}: {hostname}")
        for cdn, keywords in CDN_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in hostname.lower():
                    logger.info(f"{ip} - CDN detectado por PTR: {cdn}")
                    return cdn
    except Exception as e:
        logger.debug(f"No se pudo realizar PTR lookup para {ip}: {e}")
    return None

def cdn_validation_by_whois(ip: str) -> str:
    """
    Ejecuta una consulta whois para la IP y analiza el resultado en busca de indicadores
    de que la IP pertenece a un CDN.
    
    Nota: Una implementación real debería procesar la salida de whois de forma robusta.
    """
    try:
        process = subprocess.run(["whois", ip], capture_output=True, text=True, timeout=10)
        output = process.stdout.lower()
        logger.debug(f"Resultado whois para {ip}: {output[:200]}...")
        for cdn, keywords in CDN_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in output:
                    logger.info(f"{ip} - CDN detectado por WHOIS: {cdn}")
                    return cdn
    except Exception as e:
        logger.debug(f"Error en whois para {ip}: {e}")
    return None

def cdn_validation_by_headers_and_cookies_name(ip: str, domain: str) -> str:
    """
    Realiza una petición HTTP/HTTPS forzando el header Host para el dominio indicado
    y analiza las cabeceras de respuesta en busca de patrones característicos de CDNs.
    
    Nota: Esta función podría extenderse con validaciones de cookies y otros headers.
    """
    url = f"https://{ip}"
    headers = {
        "Host": domain,
        "User-Agent": "CDN-Jump/0.1",
    }
    try:
        response = requests.get(url, headers=headers, timeout=5, verify=False)
        logger.debug(f"Cabeceras HTTP para {ip} (Host: {domain}): {response.headers}")
        header_str = " ".join([f"{k}: {v}" for k, v in response.headers.items()]).lower()
        for cdn, patterns in CDN_KEYWORDS.items():
            for pattern in patterns:
                if re.search(pattern, header_str):
                    logger.info(f"{ip} - CDN detectado por cabeceras HTTP: {cdn}")
                    return cdn
    except Exception as e:
        logger.debug(f"Error en petición HTTP para {ip}: {e}")
    return None

def cdn_validation(ip_list: list, domain: str) -> dict:
    """
    Para cada IP en la lista, intenta detectar si pertenece a un CDN utilizando
    las tres técnicas: PTR lookup, consulta whois y análisis de cabeceras HTTP.
    
    Retorna:
      - dict: Diccionario con cada IP y el resultado de la detección.
    """
    results = {}
    for ip in ip_list:
        logger.info(f"Analizando {ip}...")
        cdn_name = cdn_validation_by_PTR_register(ip)
        if not cdn_name:
            cdn_name = cdn_validation_by_whois(ip)
        if not cdn_name:
            cdn_name = cdn_validation_by_headers_and_cookies_name(ip, domain)
        if not cdn_name:
            cdn_name = "Potential CDN bypass"
            logger.info(f"{ip} - {cdn_name}")
        results[ip] = cdn_name
    return results
