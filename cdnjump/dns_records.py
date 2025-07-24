import dns.resolver
import logging

def get_dns_a_records(domain: str, resolver: str = "1.1.1.1") -> list:
    """
    Realiza una consulta DNS para obtener los registros A del dominio especificado.

    Parámetros:
      - domain (str): El dominio a consultar.
      - resolver (str): La dirección IP del servidor DNS a utilizar (por defecto, "1.1.1.1").

    Retorna:
      - list: Una lista de direcciones IP (registros A) asociados al dominio.

    Lanza:
      - Exception: En caso de error durante la consulta DNS.
    """
    try:
        # Crear una instancia del resolvedor y asignar el servidor DNS deseado
        resolver_instance = dns.resolver.Resolver()
        resolver_instance.nameservers = [resolver]

        # Realizar la consulta para obtener registros A
        answers = resolver_instance.resolve(domain, "A")
        ip_list = [rdata.to_text() for rdata in answers]

        logging.info(f"Registros A para {domain}: {ip_list}")
        return ip_list
    except Exception as e:
        logging.error(f"Error al obtener registros A para {domain}: {e}")
        raise Exception(f"Error al obtener registros A para {domain}: {e}")
