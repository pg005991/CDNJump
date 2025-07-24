import os
import datetime
import logging
from pathlib import Path
from cdnjump.dns_records import get_dns_a_records
from cdnjump.api.virustotal import vt_get_dns_history, vt_get_certificates_history
from cdnjump.api.censys import censys_search_ip_by_certificates
from cdnjump.validation import read_and_normalize_html, similarity_percentage
from cdnjump.cdn import cdn_validation

def main_logic(domain=None, file=None, intensive=False, censys=False, virustotal=False, verbose=False):
    """
    Orquesta el análisis de dominios.
    
    Maneja dominios únicos o ficheros de dominios y, según las banderas,
    activa los distintos modos de escaneo.
    """
    # Configuración de logging
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Crear directorios base para resultados y scans
    base_dir = Path.cwd()
    results_dir = base_dir / "results"
    scans_dir = base_dir / "scans"
    results_dir.mkdir(exist_ok=True)
    scans_dir.mkdir(exist_ok=True)
    
    logging.info(f"Resultados se almacenarán en: {results_dir}")
    
    try:
        if domain:
            process_domain(domain, scans_dir, results_dir, intensive, censys, virustotal, verbose)
        elif file:
            with open(file, "r", encoding="utf-8") as f:
                domains = [line.strip() for line in f if line.strip()]
            for d in domains:
                process_domain(d, scans_dir, results_dir, intensive, censys, virustotal, verbose)
        else:
            logging.error("No se proporcionó ni un dominio ni un fichero con dominios.")
            return
    except Exception as e:
        logging.error(f"Error en la ejecución general: {e}")
    
    logging.info("Análisis completado.")

def process_domain(domain, scans_dir, results_dir, intensive, censys, virustotal, verbose):
    """
    Procesa el análisis para un dominio individual.
    
    Se crean directorios específicos para el dominio, se muestra un banner,
    y se ejecutan las funciones de consulta y validación según el modo seleccionado.
    """
    logging.info(f"\nIniciando análisis para: {domain}")
    
    domain_dir = scans_dir / domain
    domain_dir.mkdir(exist_ok=True)
    logs_dir = domain_dir / ".logs"
    logs_dir.mkdir(exist_ok=True)
    
    banner = f"""
    =====================================
           CDN-Jump: Escaneo de {domain}
    =====================================
    """
    logging.info(banner)
    
    # Consulta DNS: se obtiene la lista de registros A
    dns_records = get_dns_a_records(domain)
    logging.info(f"Registros DNS obtenidos: {dns_records}")
    
    # Consulta VirusTotal (modo intensivo vs. básico)
    if intensive:
        vt_ips = vt_get_dns_history(domain)
        vt_certs = vt_get_certificates_history(domain)
        logging.info(f"Modo intensivo VT: {vt_ips}, Certificados: {vt_certs}")
        ip_list = list(set(vt_ips))  # Aquí se podría combinar con resultados de certificados
    else:
        vt_ips = vt_get_dns_history(domain)
        logging.info(f"Modo básico VT: {vt_ips}")
        ip_list = vt_ips

    # Si se activa Censys, combinar resultados de ambas fuentes
    if censys:
        censys_ips = censys_search_ip_by_certificates(domain)
        logging.info(f"Resultados Censys: {censys_ips}")
        ip_list = list(set(ip_list + censys_ips))
    
    # Aquí se pueden incluir validaciones adicionales de contenido, etc.
    
    ip_list = sorted(set(ip_list))
    logging.info(f"IP finales a validar tras combinaciones y filtrados: {ip_list}")
    
    # Validación de CDNs: se obtiene un diccionario con la detección para cada IP.
    cdn_results = cdn_validation(ip_list, domain)
    for ip, result in cdn_results.items():
        logging.info(f"{ip}: {result}")
    
    # Guardar los resultados en un fichero de resultados
    results_filename = results_dir / f"results_{domain}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(results_filename, "w", encoding="utf-8") as out:
        out.write(f"Resultados para {domain}:\n")
        for ip, result in cdn_results.items():
            out.write(f"{ip}: {result}\n")
    
    logging.info(f"Análisis para {domain} completado.\n")

if __name__ == "__main__":
    # Ejemplo de ejecución para un dominio único en modo verbose.
    main_logic(domain="ejemplo.com", intensive=True, censys=True, virustotal=True, verbose=True)
