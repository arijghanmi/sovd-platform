# -*- coding: utf-8 -*-
# conftest.py - Configuration pytest globale
# AUTO-GENERE par generate_tests.py

import pytest
import requests

BASE_URL = "http://localhost:8081"

def pytest_configure(config):
    config.addinivalue_line(
        "markers", "sovd: mark test as ASAM SOVD compliance test"
    )

@pytest.fixture(scope="session", autouse=True)
def check_server():
    """Verifie que le serveur SOVD est accessible avant les tests"""
    try:
        r = requests.get(f"{BASE_URL}/ecu", timeout=3)
        assert r.status_code == 200, "Serveur SOVD inaccessible"
    except Exception as e:
        pytest.exit(f"Serveur SOVD non accessible sur {BASE_URL} : {e}")
