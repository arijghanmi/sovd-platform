# -*- coding: utf-8 -*-
# ============================================================
# generate_tests.py - Generateur Automatique de Tests SOVD
#
# Usage : python generate_tests.py
#
# Lit ecu1_config.yaml ET ecu2_config.yaml
# Genere les fichiers de tests pytest :
#   tests/test_ecu1.py
#   tests/test_ecu2.py
#
# Reference ASAM SOVD V1.0.0
# ============================================================

import yaml, os, sys
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "tests")
ECU_CONFIGS = [
    os.path.join(os.path.dirname(__file__), "ecu1_config.yaml"),
    os.path.join(os.path.dirname(__file__), "ecu2_config.yaml"),
]

def load_config(path):
    with open(path, "r") as f:
        return yaml.safe_load(f)

def write_file(filename, content):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [GENERATED] {filename}")

def header(ecu_id, src):
    return f'''# -*- coding: utf-8 -*-
# ============================================================
# test_ecu{ecu_id}.py
# AUTO-GENERE par generate_tests.py - Source: {src}
# Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Reference ASAM SOVD V1.0.0
# NE PAS MODIFIER MANUELLEMENT
# Execution : pytest test_ecu{ecu_id}.py -v
# ============================================================

import pytest
import requests

BASE_URL = "http://localhost:8081"

'''

def generate_tests(cfg, src):
    ecu      = cfg["ecu"]
    eid      = ecu["entity_id"]
    ec       = ecu["entity_collection"]
    data_ids = [d["id"] for d in ecu["data"]["initial_data"]]
    fault_types = ecu["faults"]["types"]
    resources   = [r["name"] for r in ecu["discovery"]["resources"]]
    update_ids  = [u["id"] for u in ecu["updates"]["initial_catalog"]]
    sse_id      = ecu["data"]["sse"]["data_id"]

    code = header(eid, src)

    # --------------------------------------------------------
    # DISCOVERY
    # --------------------------------------------------------
    code += f'''
# ============================================================
# DISCOVERY - ASAM SOVD Section 5.1
# ============================================================

def test_discovery_list_all_ecus():
    """GET /ecu - Liste tous les ECUs disponibles"""
    r = requests.get(f"{{BASE_URL}}/{ec}")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    ids = [e["id"] for e in data["items"]]
    assert "{eid}" in ids

def test_discovery_ecu{eid}_entity():
    """GET /ecu/{eid} - Entite ECU {eid}"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "{eid}"

'''

    # --------------------------------------------------------
    # CAPABILITIES
    # --------------------------------------------------------
    code += f'''
# ============================================================
# CAPABILITIES - ASAM SOVD Section 5.2
# ============================================================

def test_capabilities_ecu{eid}():
    """GET /ecu/{eid}/docs - Capability description"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/docs")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu_id"] == "{eid}"
    assert "resources" in data
    assert "data_ids" in data
    assert data["sovd_standard"] == "ASAM SOVD V1.0.0"

def test_capabilities_ecu{eid}_include_schema():
    """GET /ecu/{eid}/docs?include-schema=true - OpenAPI schema"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/docs", params={{"include-schema": "true"}})
    assert r.status_code == 200

def test_config_ecu{eid}():
    """GET /ecu/{eid}/config - Config YAML source of truth"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/config")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu"]["entity_id"] == "{eid}"

'''

    # --------------------------------------------------------
    # FAULTS
    # --------------------------------------------------------
    code += f'''
# ============================================================
# FAULT HANDLING - ASAM SOVD Section 6.3
# ============================================================

def test_get_faults_ecu{eid}():
    """GET /ecu/{eid}/faults - Liste les faults"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/faults")
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data
    assert "total_faults" in data
    assert "counts_by_type" in data

'''
    for ft in fault_types:
        code += f'''def test_get_faults_ecu{eid}_scope_{ft.lower()}():
    """GET /ecu/{eid}/faults?scope={ft} - Filtre par type {ft}"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/faults", params={{"scope": "{ft}"}})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

'''

    code += f'''def test_add_fault_ecu{eid}():
    """POST /ecu/{eid}/faults - Injection DTC"""
    payload = {{
        "faultCode": "TEST001",
        "description": "Test fault injected by pytest",
        "severity": 1,
        "component": "test",
        "dtc_type": "ACTIVE"
    }}
    r = requests.post(f"{{BASE_URL}}/{ec}/{eid}/faults", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "fault" in data

def test_get_fault_by_id_ecu{eid}():
    """GET /ecu/{eid}/faults/TEST001 - Fault par ID"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/faults/TEST001")
    assert r.status_code == 200
    data = r.json()
    assert data["found"] == True

def test_clear_faults_ecu{eid}():
    """DELETE /ecu/{eid}/faults - Suppression faults"""
    r = requests.delete(f"{{BASE_URL}}/{ec}/{eid}/faults")
    assert r.status_code == 200
    data = r.json()
    assert "cleared" in data["message"]

'''

    # --------------------------------------------------------
    # DATA
    # --------------------------------------------------------
    code += f'''
# ============================================================
# DATA RETRIEVAL - ASAM SOVD Section 6.1
# ============================================================

def test_get_all_data_ecu{eid}():
    """GET /ecu/{eid}/data - Tous les data items"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/data")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

'''
    for did in data_ids:
        code += f'''def test_get_data_{did.replace("-","_")}_ecu{eid}():
    """GET /ecu/{eid}/data/{did} - Valeur {did}"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/data/{did}")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

'''

    code += f'''def test_update_data_ecu{eid}():
    """PUT /ecu/{eid}/data/{data_ids[0]} - Mise a jour valeur"""
    payload = {{"value": 42}}
    r = requests.put(f"{{BASE_URL}}/{ec}/{eid}/data/{data_ids[0]}", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "updated"

def test_get_data_invalid_id_ecu{eid}():
    """GET /ecu/{eid}/data/nonexistent - ID inexistant retourne 404"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/data/nonexistent_data_id_xyz")
    assert r.status_code == 404

'''

    # --------------------------------------------------------
    # SSE
    # --------------------------------------------------------
    code += f'''
# ============================================================
# SSE (ResponseOnEvent) - ASAM SOVD Section 6.5
# ============================================================

def test_sse_endpoint_ecu{eid}_exists():
    """GET /ecu/{eid}/data/{sse_id}/events - SSE endpoint accessible"""
    import threading, time
    result = {{}}
    def fetch():
        try:
            r = requests.get(
                f"{{BASE_URL}}/{ec}/{eid}/data/{sse_id}/events",
                stream=True, timeout=2
            )
            result["status"] = r.status_code
            result["content_type"] = r.headers.get("content-type", "")
        except Exception as e:
            result["error"] = str(e)
    t = threading.Thread(target=fetch)
    t.start()
    t.join(timeout=3)
    assert result.get("status") == 200
    assert "text/event-stream" in result.get("content_type", "")

'''

    # --------------------------------------------------------
    # LOGS
    # --------------------------------------------------------
    code += f'''
# ============================================================
# LOGGING - ASAM SOVD Section 6.4
# ============================================================

def test_get_logs_ecu{eid}():
    """GET /ecu/{eid}/logs - Liste les logs"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/logs")
    assert r.status_code == 200
    data = r.json()
    assert "entries" in data
    assert "total" in data

def test_get_logs_with_limit_ecu{eid}():
    """GET /ecu/{eid}/logs?limit=5 - Limite les logs"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/logs", params={{"limit": 5}})
    assert r.status_code == 200
    data = r.json()
    assert len(data["entries"]) <= 5

def test_clear_logs_ecu{eid}():
    """DELETE /ecu/{eid}/logs - Suppression logs"""
    r = requests.delete(f"{{BASE_URL}}/{ec}/{eid}/logs")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "cleared"

'''

    # --------------------------------------------------------
    # UPDATES
    # --------------------------------------------------------
    code += f'''
# ============================================================
# SOFTWARE UPDATES (OTA) - ASAM SOVD Section 6.6
# ============================================================

def test_get_updates_ecu{eid}():
    """GET /ecu/{eid}/updates - Catalogue OTA"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/updates")
    assert r.status_code == 200
    data = r.json()
    assert "updates" in data
    assert data["total"] > 0

'''
    for uid in update_ids:
        code += f'''def test_install_update_{uid.replace("-","_")}_ecu{eid}():
    """POST /ecu/{eid}/updates - Installer {uid}"""
    payload = {{"id": "{uid}"}}
    r = requests.post(f"{{BASE_URL}}/{ec}/{eid}/updates", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "{uid}"
    assert data["status"] == "installing"

def test_update_status_{uid.replace("-","_")}_ecu{eid}():
    """GET /ecu/{eid}/updates/{uid} - Statut OTA {uid}"""
    r = requests.get(f"{{BASE_URL}}/{ec}/{eid}/updates/{uid}")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "progress" in data

'''

    return code


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  SOVD Test Generator")
    print(f"  Output : {OUTPUT_DIR}")
    print("=" * 60)

    configs = []
    for path in ECU_CONFIGS:
        if not os.path.exists(path):
            print(f"  ERREUR : {path} introuvable"); sys.exit(1)
        cfg = load_config(path)
        eid = cfg["ecu"]["entity_id"]
        print(f"  Charge : ECU {eid} - {os.path.basename(path)}")
        configs.append((cfg, os.path.basename(path)))

    print()

    for cfg, src in configs:
        eid = cfg["ecu"]["entity_id"]
        write_file(f"test_ecu{eid}.py", generate_tests(cfg, src))

    # Generer conftest.py
    conftest = '''# -*- coding: utf-8 -*-
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
'''
    write_file("conftest.py", conftest)

    print()
    print("  DONE - Fichiers generes :")
    for cfg, _ in configs:
        eid = cfg["ecu"]["entity_id"]
        print(f"    tests/test_ecu{eid}.py")
    print(f"    tests/conftest.py")
    print()
    print("  Pour executer :")
    print("    cd tests")
    print("    pytest test_ecu1.py -v")
    print("    pytest test_ecu2.py -v")
    print("    pytest -v  (tous les tests)")
    print("=" * 60)
