import pytest
import logging
from cdnjump.cdn import cdn_validation

def test_cdn_validation_logs(caplog):
    """
    Verifica que, para cada IP proporcionada, la función cdn_validation
    registre un mensaje que contenga "Posible bypass CDN detectado".
    """
    # Lista de IPs de prueba
    ip_list = ["192.0.2.1", "203.0.113.5", "198.51.100.42"]
    
    with caplog.at_level(logging.INFO):
        cdn_validation(ip_list)
    
    # Para cada IP se comprueba que exista un mensaje adecuado
    for ip in ip_list:
        mensajes = [
            record.message for record in caplog.records 
            if ip in record.message and "Posible bypass CDN detectado" in record.message
        ]
        assert len(mensajes) > 0, f"No se encontró mensaje de bypass para la IP {ip}"

def test_cdn_validation_empty(caplog):
    """
    Verifica que si se pasa una lista vacía a cdn_validation no se generen mensajes
    de bypass.
    """
    ip_list = []
    with caplog.at_level(logging.INFO):
        cdn_validation(ip_list)
    
    # No deberían registrarse mensajes de bypass cuando la lista está vacía
    mensajes = [
        record.message for record in caplog.records 
        if "Posible bypass CDN detectado" in record.message
    ]
    assert len(mensajes) == 0, "No se esperaban mensajes de bypass con lista vacía"
