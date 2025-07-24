import pytest
import requests
import ipaddress
from cdnjump.api.virustotal import vt_get_ip_as_owner, vt_get_dns_history, vt_get_certificates_history
from cdnjump.api.censys import censys_search_certificates

# Clase auxiliar para simular la respuesta de requests.get
class FakeResponse:
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code

    def json(self):
        return self._json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise requests.HTTPError(f"{self.status_code} Error")

# Funciones fake para simular respuestas de la API de VirusTotal

def fake_requests_get_vt_ip(*args, **kwargs):
    data = {
        "data": {
            "attributes": {
                "as_owner": "Fake ISP Inc."
            }
        }
    }
    return FakeResponse(data, 200)

def fake_requests_get_vt_dns(*args, **kwargs):
    data = {
        "data": [
            {"attributes": {"ip_address": "1.1.1.1"}},
            {"attributes": {"ip_address": "8.8.8.8"}}
        ],
        "links": {"next": None}
    }
    return FakeResponse(data, 200)

def fake_requests_get_vt_cert(*args, **kwargs):
    data = {
        "data": [
            {"attributes": {"thumbprint_sha256": "fp1"}},
            {"attributes": {"thumbprint_sha256": "fp2"}}
        ],
        "links": {"next": None}
    }
    return FakeResponse(data, 200)

# Función fake para simular la respuesta de la API de Censys para certificados,
# utilizando la muestra de respuesta proporcionada.
def fake_requests_get_censys_cert(*args, **kwargs):
    data = {
      "code": 200,
      "status": "OK",
      "result": {
        "query": "parsed.subject.country: AU",
        "total": 50000,
        "duration_ms": 356,
        "hits": [
          {
            "fingerprint_sha256": "9b00121b4e85d50667ded1a8aa39855771bdb67ceca6f18726b49374b41f0041",
            "parsed": {
              "issuer_dn": "C=US, O=Let's Encrypt, CN=R3",
              "subject_dn": "CN=www.kgcontracting.co",
              "validity_period": {
                "not_before": "2022-12-31T11:37:55Z",
                "not_after": "2023-03-31T11:37:54Z"
              }
            },
            "names": [
              [
                "kgcontracting.co",
                "www.kgcontracting.co"
              ]
            ]
          }
        ]
      },
      "links": {
        "prev": "prevCursorToken",
        "next": "nextCursorToken"
      }
    }
    return FakeResponse(data, 200)

# Tests para las funciones de VirusTotal

def test_vt_get_ip_as_owner(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_requests_get_vt_ip)
    result = vt_get_ip_as_owner("1.2.3.4")
    assert result == "Fake ISP Inc.", f"Se esperaba 'Fake ISP Inc.' y se obtuvo {result}"

def test_vt_get_dns_history(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_requests_get_vt_dns)
    result = vt_get_dns_history("example.com", limit=40)
    expected = ["1.1.1.1", "8.8.8.8"]
    assert result == expected, f"Se esperaba {expected} y se obtuvo {result}"

def test_vt_get_certificates_history(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_requests_get_vt_cert)
    result = vt_get_certificates_history("example.com", limit=40)
    expected = ["fp1", "fp2"]
    assert result == expected, f"Se esperaba {expected} y se obtuvo {result}"

# Test para la función de Censys usando la muestra de respuesta
def test_censys_search_certificates(monkeypatch):
    monkeypatch.setattr(requests, "get", fake_requests_get_censys_cert)
    result = censys_search_certificates("example.com", limit=50)
    expected = ["9b00121b4e85d50667ded1a8aa39855771bdb67ceca6f18726b49374b41f0041"]
    assert result == expected, f"Se esperaba {expected} y se obtuvo {result}"
