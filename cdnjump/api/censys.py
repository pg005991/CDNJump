import os
import requests
import logging
from dotenv import load_dotenv

# Cargar variables de entorno del fichero .env
load_dotenv()

# Obtener variables necesarias para la API de Censys
CENSYS_API_ID = os.getenv("CENSYS_API_ID")
CENSYS_API_SECRET = os.getenv("CENSYS_API_SECRET")
CENSYS_URL_API = os.getenv("CENSYS_URL_API")  # Ejemplo: "https://search.censys.io"
if not all([CENSYS_API_ID, CENSYS_API_SECRET, CENSYS_URL_API]):
    raise Exception("Faltan variables de entorno para la API de Censys.")

# Configuración de logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Agregamos el header User-Agent
HEADERS = {
    "Content-Type": "application/json",
    "Referer": CENSYS_URL_API,
    "User-Agent": "CDN-Jump/0.1",
}

def censys_search_certificates(domain: str, limit: int = 50) -> list:
    """
    Realiza una búsqueda de certificados en la API de Censys relacionados con el dominio.
    
    Se utiliza una query que busca en 'parsed.names' para encontrar certificados donde
    el dominio aparezca entre los nombres del certificado.
    
    Parámetros:
      - domain (str): Dominio a buscar.
      - limit (int): Número de resultados por petición (por defecto 50).
      
    Retorna:
      - list: Lista de huellas SHA256 (fingerprint_sha256) extraídas de los certificados.
    """
    url = f"{CENSYS_URL_API}/api/v2/certificates/search"
    
    params = {
        "q": f"parsed.names: {domain}",
        "fields": "fingerprint_sha256,names,parsed.issuer.organization,parsed.subject.postal_code",
        "per_page": limit,
    }
    
    fingerprints = []
    while url:
        try:
            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                auth=(CENSYS_API_ID, CENSYS_API_SECRET),
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            hits = data.get("result", {}).get("hits", [])
            for hit in hits:
                fp = hit.get("fingerprint_sha256")
                if fp:
                    fingerprints.append(fp)
            logger.info(f"Encontrados {len(hits)} certificados en esta página para {domain}")
            
            # Actualizar URL para paginación
            url = data.get("result", {}).get("links", {}).get("next")
            params = {}  # Una vez que usamos links.next, no es necesario reenviar params
        except Exception as e:
            logger.error(f"Error al buscar certificados en Censys para {domain}: {e}")
            raise
    return fingerprints

def censys_search_ip_by_certificates(domain: str, limit: int = 50) -> list:
    """
    Realiza una búsqueda de IPs en la API de Censys basada en certificados del dominio.
    
    Esta función busca certificados relacionados con el dominio y extrae las IPs
    asociadas a esos certificados.
    
    Parámetros:
      - domain (str): Dominio a buscar.
      - limit (int): Número de resultados por petición (por defecto 50).
      
    Retorna:
      - list: Lista de direcciones IP extraídas de los certificados.
    """
    # Primero obtenemos los certificados
    certificates = censys_search_certificates(domain, limit)
    
    # Por ahora, como no tenemos una función para extraer IPs directamente
    # de los certificados, retornamos una lista vacía
    # En una implementación completa, aquí se buscarían las IPs asociadas
    # a los certificados encontrados
    
    logger.info(f"Certificados encontrados para {domain}: {len(certificates)}")
    logger.warning("Extracción de IPs desde certificados no implementada completamente")
    
    return []  # Placeholder - en implementación real extraería IPs de certificados

# Ejemplo de uso (para pruebas locales)
if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG, format="[%(asctime)s] %(levelname)s: %(message)s", datefmt="%H:%M:%S")
    
    if len(sys.argv) < 2:
        print("Uso: python censys_cert_search.py <domain>")
        sys.exit(1)
    
    domain = sys.argv[1]
    try:
        cert_fingerprints = censys_search_certificates(domain)
        print(f"Certificados encontrados para {domain}:")
        for fp in cert_fingerprints:
            print(fp)
    except Exception as e:
        print("Error:", e)
