import os
import datetime
import logging
from pathlib import Path
from cdnjump.dns_records import get_dns_a_records
from cdnjump.api.virustotal import vt_get_dns_history, vt_get_certificates_history
from cdnjump.api.censys import censys_search_ip_by_certificates
from cdnjump.validation import read_and_normalize_html, similarity_percentage
from cdnjump.cdn import cdn_validation
from cdnjump.logger import DomainLogger, setup_global_logging

def main_logic(domain=None, file=None, intensive=False, censys=False, virustotal=False, verbose=False):
    """
    Orquesta el análisis de dominios.
    
    Maneja dominios únicos o ficheros de dominios y, según las banderas,
    activa los distintos modos de escaneo.
    """
    # Configuración de logging global
    setup_global_logging(verbose)
    
    # Crear directorios base para resultados y scans
    base_dir = Path.cwd()
    results_dir = base_dir / "results"
    scans_dir = base_dir / "scans"
    results_dir.mkdir(exist_ok=True)
    scans_dir.mkdir(exist_ok=True)
    
    logging.info(f"📁 Directorio de resultados: {results_dir}")
    
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
    
    Se crean directorios específicos para el dominio, se configura logging específico,
    y se ejecutan las funciones de consulta y validación según el modo seleccionado.
    """
    # Crear logger específico para el dominio
    domain_logger = DomainLogger(results_dir, domain, verbose)
    domain_logger.log_banner(domain)
    
    try:
        # Consulta DNS: se obtiene la lista de registros A
        dns_records = get_dns_a_records(domain)
        domain_logger.log_dns_results(dns_records)
    
        # Consulta VirusTotal (modo intensivo vs. básico)
        if intensive:
            vt_ips = vt_get_dns_history(domain)
            vt_certs = vt_get_certificates_history(domain)
            domain_logger.log_virustotal_results(vt_ips, vt_certs, intensive=True)
            ip_list = list(set(vt_ips))  # Aquí se podría combinar con resultados de certificados
        else:
            vt_ips = vt_get_dns_history(domain)
            domain_logger.log_virustotal_results(vt_ips, intensive=False)
            ip_list = vt_ips

        # Si se activa Censys, combinar resultados de ambas fuentes
        if censys:
            censys_ips = censys_search_ip_by_certificates(domain)
            domain_logger.log_censys_results(censys_ips)
            ip_list = list(set(ip_list + censys_ips))
        
        # Aquí se pueden incluir validaciones adicionales de contenido, etc.
        
        ip_list = sorted(set(ip_list))
        domain_logger.log_combined_results(ip_list)
        
        # Validación de CDNs: se obtiene un diccionario con la detección para cada IP.
        cdn_results = cdn_validation(ip_list, domain)
        domain_logger.log_cdn_results(cdn_results)
        
        # Registrar resumen final
        domain_logger.log_summary(cdn_results)
        
        domain_logger.info(f"✅ Análisis completado para {domain}")
        domain_logger.info(f"📄 Log guardado en: {domain_logger.get_log_file_path()}")
        
    except Exception as e:
        domain_logger.error(f"❌ Error durante el análisis de {domain}: {e}")
        raise

if __name__ == "__main__":
    # Ejemplo de ejecución para un dominio único en modo verbose.
    main_logic(domain="ejemplo.com", intensive=True, censys=True, virustotal=True, verbose=True)
