import pytest
import ipaddress
from cdnjump.dns_records import get_dns_a_records

def test_get_dns_a_records_return_type():
    """
    Verifica que la función get_dns_a_records retorne una lista.
    """
    domain = "example.com"
    records = get_dns_a_records(domain)
    assert isinstance(records, list), "El resultado debe ser una lista de registros DNS"

def test_get_dns_a_records_not_empty():
    """
    Verifica que la lista de registros DNS no esté vacía.
    """
    domain = "example.com"
    records = get_dns_a_records(domain)
    assert len(records) > 0, "La lista de registros DNS no debe estar vacía"

def test_get_dns_a_records_values():
    """
    Verifica que cada registro retornado sea una dirección IP válida.
    """
    domain = "example.com"
    records = get_dns_a_records(domain)
    for record in records:
        try:
            # Si no es una IP válida, ipaddress.ip_address lanzará una excepción.
            ipaddress.ip_address(record)
        except ValueError:
            pytest.fail(f"El registro '{record}' no es una dirección IP válida.")
