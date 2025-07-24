import os
import requests
import logging
from dotenv import load_dotenv

# Cargar variables de entorno del fichero .env
load_dotenv()

# Obtener la clave API desde la variable de entorno
VT_API_KEY = os.getenv("VT_API_KEY")
if not VT_API_KEY:
    raise Exception("No se encontró la variable VT_API_KEY en el fichero .env")

VT_BASE_URL = "https://www.virustotal.com/api/v3"

logger = logging.getLogger(__name__)

def vt_get_ip_as_owner(ip: str) -> str:
    """
    Consulta la API de VirusTotal para obtener el 'as_owner' de una IP.

    Parámetros:
      - ip (str): Dirección IP a consultar.

    Retorna:
      - str: El propietario del AS de la IP.

    Lanza:
      - Exception: Si la consulta falla o no se encuentra el campo esperado.
    """
    url = f"{VT_BASE_URL}/ip_addresses/{ip}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        as_owner = data.get("data", {}).get("attributes", {}).get("as_owner")
        if as_owner is None:
            raise Exception(f"No se encontró 'as_owner' en la respuesta para la IP {ip}")
        logger.info(f"IP {ip} - AS Owner: {as_owner}")
        return as_owner
    except Exception as e:
        logger.error(f"Error al consultar as_owner para {ip}: {e}")
        raise

def vt_get_dns_history(domain: str, limit: int = 40) -> list:
    """
    Consulta la API de VirusTotal para obtener el historial de resoluciones DNS de un dominio.
    Gestiona la paginación si existe.

    Parámetros:
      - domain (str): Dominio a consultar.
      - limit (int): Número de registros por petición (por defecto 40).

    Retorna:
      - list: Lista de direcciones IP obtenidas del historial de resoluciones.
    """
    ip_list = []
    url = f"{VT_BASE_URL}/domains/{domain}/resolutions?limit={limit}"
    headers = {"x-apikey": VT_API_KEY}
    
    while url:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            records = data.get("data", [])
            for record in records:
                ip = record.get("attributes", {}).get("ip_address")
                if ip:
                    ip_list.append(ip)
            logger.info(f"Obtenidas {len(records)} resoluciones de {domain}")
            url = data.get("links", {}).get("next")
        except Exception as e:
            logger.error(f"Error al obtener historial DNS para {domain}: {e}")
            raise

    return ip_list

def vt_get_certificates_history(domain: str, limit: int = 40) -> list:
    """
    Consulta la API de VirusTotal para obtener el historial de certificados SSL
    asociados a un dominio. Gestiona la paginación si existe.

    Parámetros:
      - domain (str): Dominio a consultar.
      - limit (int): Número de registros por petición (por defecto 40).

    Retorna:
      - list: Lista de certificados (thumbprint_sha256) extraídos del historial.
    """
    certificates = []
    url = f"{VT_BASE_URL}/domains/{domain}/historical_ssl_certificates?limit={limit}"
    headers = {"x-apikey": VT_API_KEY}

    while url:
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            records = data.get("data", [])
            for record in records:
                thumbprint = record.get("attributes", {}).get("thumbprint_sha256")
                if thumbprint:
                    certificates.append(thumbprint)
            logger.info(f"Obtenidos {len(records)} certificados para {domain}")
            url = data.get("links", {}).get("next")
        except Exception as e:
            logger.error(f"Error al obtener certificados para {domain}: {e}")
            raise

    return certificates

# Ejemplo de uso (para pruebas locales)
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S")
    if len(sys.argv) < 2:
        print("Uso: python virustotal.py <domain>")
        sys.exit(1)

    domain = sys.argv[1]

    try:
        dns_history = vt_get_dns_history(domain)
        print("Historial DNS:", dns_history)

        cert_history = vt_get_certificates_history(domain)
        print("Historial Certificados:", cert_history)
    except Exception as e:
        print("Error:", e)
