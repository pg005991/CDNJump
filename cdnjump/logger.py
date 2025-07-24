import logging
import datetime
from pathlib import Path
from typing import Optional

class DomainLogger:
    """
    Clase para manejar logging específico por dominio.
    
    Crea loggers separados para cada dominio con archivos de log individuales
    que incluyen timestamp y se almacenan en la carpeta de resultados.
    """
    
    def __init__(self, results_dir: Path, domain: str, verbose: bool = False):
        """
        Inicializa el logger para un dominio específico.
        
        Args:
            results_dir: Directorio donde se guardarán los logs
            domain: Dominio a analizar
            verbose: Si activar modo verbose
        """
        self.results_dir = results_dir
        self.domain = domain
        self.verbose = verbose
        self.logger = None
        self.log_file = None
        self._setup_logger()
    
    def _setup_logger(self):
        """Configura el logger específico para el dominio."""
        # Crear nombre de archivo con timestamp
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{self.domain}_{timestamp}.log"
        self.log_file = self.results_dir / filename
        
        # Crear logger específico para el dominio
        self.logger = logging.getLogger(f"cdnjump.{self.domain}")
        self.logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        
        # Evitar duplicación de handlers
        if not self.logger.handlers:
            # Handler para archivo
            file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
            
            # Formato detallado para archivo
            file_formatter = logging.Formatter(
                '[%(asctime)s] %(name)s - %(levelname)s: %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Solo agregar handler de consola si no hay otros handlers globales
            if not logging.getLogger().handlers:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(logging.INFO)
                
                # Formato simple para consola
                console_formatter = logging.Formatter(
                    '[%(asctime)s] %(levelname)s: %(message)s',
                    datefmt='%H:%M:%S'
                )
                
                console_handler.setFormatter(console_formatter)
                self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Registra un mensaje de nivel INFO."""
        if self.logger:
            self.logger.info(message)
    
    def debug(self, message: str):
        """Registra un mensaje de nivel DEBUG."""
        if self.logger:
            self.logger.debug(message)
    
    def warning(self, message: str):
        """Registra un mensaje de nivel WARNING."""
        if self.logger:
            self.logger.warning(message)
    
    def error(self, message: str):
        """Registra un mensaje de nivel ERROR."""
        if self.logger:
            self.logger.error(message)
    
    def critical(self, message: str):
        """Registra un mensaje de nivel CRITICAL."""
        if self.logger:
            self.logger.critical(message)
    
    def log_banner(self, domain: str):
        """Registra el banner de inicio del análisis."""
        banner = f"""
{'='*60}
           CDN-Jump: Escaneo de {domain}
{'='*60}
Fecha de inicio: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Archivo de log: {self.log_file}
{'='*60}
"""
        self.info(banner)
    
    def log_dns_results(self, dns_records: list):
        """Registra los resultados de DNS."""
        self.info(f"📡 REGISTROS DNS OBTENIDOS:")
        self.info(f"   Dominio: {self.domain}")
        self.info(f"   Registros A: {dns_records}")
        self.info(f"   Total de IPs: {len(dns_records)}")
        self.info("-" * 40)
    
    def log_virustotal_results(self, vt_ips: list, vt_certs: Optional[list] = None, intensive: bool = False):
        """Registra los resultados de VirusTotal."""
        self.info(f"🔍 RESULTADOS VIRUSTOTAL:")
        self.info(f"   Modo: {'Intensivo' if intensive else 'Básico'}")
        self.info(f"   IPs históricas: {vt_ips}")
        self.info(f"   Total de IPs: {len(vt_ips)}")
        if vt_certs:
            self.info(f"   Certificados encontrados: {len(vt_certs)}")
        self.info("-" * 40)
    
    def log_censys_results(self, censys_ips: list):
        """Registra los resultados de Censys."""
        self.info(f"🔎 RESULTADOS CENSYS:")
        self.info(f"   IPs desde certificados: {censys_ips}")
        self.info(f"   Total de IPs: {len(censys_ips)}")
        self.info("-" * 40)
    
    def log_combined_results(self, ip_list: list):
        """Registra los resultados combinados."""
        self.info(f"🔄 RESULTADOS COMBINADOS:")
        self.info(f"   IPs únicas a validar: {ip_list}")
        self.info(f"   Total de IPs: {len(ip_list)}")
        self.info("-" * 40)
    
    def log_cdn_results(self, cdn_results: dict):
        """Registra los resultados de detección de CDN."""
        self.info(f"🛡️ RESULTADOS DETECCIÓN CDN:")
        for ip, result in cdn_results.items():
            status_icon = "✅" if "bypass" in str(result).lower() else "🔄"
            self.info(f"   {status_icon} {ip}: {result}")
        self.info("-" * 40)
    
    def log_summary(self, cdn_results: dict):
        """Registra un resumen final del análisis."""
        bypass_count = sum(1 for result in cdn_results.values() 
                         if "bypass" in str(result).lower())
        cdn_count = len(cdn_results) - bypass_count
        
        self.info(f"📊 RESUMEN DEL ANÁLISIS:")
        self.info(f"   Dominio analizado: {self.domain}")
        self.info(f"   Total de IPs analizadas: {len(cdn_results)}")
        self.info(f"   IPs con CDN detectado: {cdn_count}")
        self.info(f"   IPs potencial bypass: {bypass_count}")
        self.info(f"   Archivo de resultados: {self.log_file}")
        self.info(f"   Fecha de finalización: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.info("=" * 60)
    
    def get_log_file_path(self) -> Path:
        """Retorna la ruta del archivo de log."""
        return self.log_file

def setup_global_logging(verbose: bool = False):
    """
    Configura el logging global para mensajes generales.
    
    Args:
        verbose: Si activar modo verbose
    """
    # Configurar logging global básico
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        force=True  # Forzar reconfiguración
    )
