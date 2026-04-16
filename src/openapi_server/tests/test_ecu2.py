# -*- coding: utf-8 -*-
# ============================================================
# test_ecu2.py
# AUTO-GENERE par generate_tests.py - Source: ecu2_config.yaml
# Date: 2026-04-15 16:25:31
# Reference ASAM SOVD V1.0.0
# NE PAS MODIFIER MANUELLEMENT
# Execution : pytest test_ecu2.py -v
# ============================================================

import pytest
import requests

BASE_URL = "http://localhost:8081"


# ============================================================
# DISCOVERY - ASAM SOVD Section 5.1
# ============================================================

def test_discovery_list_all_ecus():
    """GET /ecu - Liste tous les ECUs disponibles"""
    r = requests.get(f"{BASE_URL}/ecu")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data
    ids = [e["id"] for e in data["items"]]
    assert "2" in ids

def test_discovery_ecu2_entity():
    """GET /ecu/2 - Entite ECU 2"""
    r = requests.get(f"{BASE_URL}/ecu/2")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "2"


# ============================================================
# CAPABILITIES - ASAM SOVD Section 5.2
# ============================================================

def test_capabilities_ecu2():
    """GET /ecu/2/docs - Capability description"""
    r = requests.get(f"{BASE_URL}/ecu/2/docs")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu_id"] == "2"
    assert "resources" in data
    assert "data_ids" in data
    assert data["sovd_standard"] == "ASAM SOVD V1.0.0"

def test_capabilities_ecu2_include_schema():
    """GET /ecu/2/docs?include-schema=true - OpenAPI schema"""
    r = requests.get(f"{BASE_URL}/ecu/2/docs", params={"include-schema": "true"})
    assert r.status_code == 200

def test_config_ecu2():
    """GET /ecu/2/config - Config YAML source of truth"""
    r = requests.get(f"{BASE_URL}/ecu/2/config")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu"]["entity_id"] == "2"


# ============================================================
# FAULT HANDLING - ASAM SOVD Section 6.3
# ============================================================

def test_get_faults_ecu2():
    """GET /ecu/2/faults - Liste les faults"""
    r = requests.get(f"{BASE_URL}/ecu/2/faults")
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data
    assert "total_faults" in data
    assert "counts_by_type" in data

def test_get_faults_ecu2_scope_active():
    """GET /ecu/2/faults?scope=ACTIVE - Filtre par type ACTIVE"""
    r = requests.get(f"{BASE_URL}/ecu/2/faults", params={"scope": "ACTIVE"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_get_faults_ecu2_scope_pending():
    """GET /ecu/2/faults?scope=PENDING - Filtre par type PENDING"""
    r = requests.get(f"{BASE_URL}/ecu/2/faults", params={"scope": "PENDING"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_get_faults_ecu2_scope_permanent():
    """GET /ecu/2/faults?scope=PERMANENT - Filtre par type PERMANENT"""
    r = requests.get(f"{BASE_URL}/ecu/2/faults", params={"scope": "PERMANENT"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_add_fault_ecu2():
    """POST /ecu/2/faults - Injection DTC"""
    payload = {
        "faultCode": "TEST001",
        "description": "Test fault injected by pytest",
        "severity": 1,
        "component": "test",
        "dtc_type": "ACTIVE"
    }
    r = requests.post(f"{BASE_URL}/ecu/2/faults", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "fault" in data

def test_get_fault_by_id_ecu2():
    """GET /ecu/2/faults/TEST001 - Fault par ID"""
    r = requests.get(f"{BASE_URL}/ecu/2/faults/TEST001")
    assert r.status_code == 200
    data = r.json()
    assert data["found"] == True

def test_clear_faults_ecu2():
    """DELETE /ecu/2/faults - Suppression faults"""
    r = requests.delete(f"{BASE_URL}/ecu/2/faults")
    assert r.status_code == 200
    data = r.json()
    assert "cleared" in data["message"]


# ============================================================
# DATA RETRIEVAL - ASAM SOVD Section 6.1
# ============================================================

def test_get_all_data_ecu2():
    """GET /ecu/2/data - Tous les data items"""
    r = requests.get(f"{BASE_URL}/ecu/2/data")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_data_gear_ecu2():
    """GET /ecu/2/data/gear - Valeur gear"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/gear")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_oil_temp_ecu2():
    """GET /ecu/2/data/oil_temp - Valeur oil_temp"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/oil_temp")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_oil_pressure_ecu2():
    """GET /ecu/2/data/oil_pressure - Valeur oil_pressure"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/oil_pressure")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_torque_ecu2():
    """GET /ecu/2/data/torque - Valeur torque"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/torque")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_efficiency_ecu2():
    """GET /ecu/2/data/efficiency - Valeur efficiency"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/efficiency")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_update_data_ecu2():
    """PUT /ecu/2/data/gear - Mise a jour valeur"""
    payload = {"value": 42}
    r = requests.put(f"{BASE_URL}/ecu/2/data/gear", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "updated"

def test_get_data_invalid_id_ecu2():
    """GET /ecu/2/data/nonexistent - ID inexistant retourne 404"""
    r = requests.get(f"{BASE_URL}/ecu/2/data/nonexistent_data_id_xyz")
    assert r.status_code == 404


# ============================================================
# SSE (ResponseOnEvent) - ASAM SOVD Section 6.5
# ============================================================

def test_sse_endpoint_ecu2_exists():
    """GET /ecu/2/data/gear/events - SSE endpoint accessible"""
    import threading, time
    result = {}
    def fetch():
        try:
            r = requests.get(
                f"{BASE_URL}/ecu/2/data/gear/events",
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


# ============================================================
# LOGGING - ASAM SOVD Section 6.4
# ============================================================

def test_get_logs_ecu2():
    """GET /ecu/2/logs - Liste les logs"""
    r = requests.get(f"{BASE_URL}/ecu/2/logs")
    assert r.status_code == 200
    data = r.json()
    assert "entries" in data
    assert "total" in data

def test_get_logs_with_limit_ecu2():
    """GET /ecu/2/logs?limit=5 - Limite les logs"""
    r = requests.get(f"{BASE_URL}/ecu/2/logs", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    assert len(data["entries"]) <= 5

def test_clear_logs_ecu2():
    """DELETE /ecu/2/logs - Suppression logs"""
    r = requests.delete(f"{BASE_URL}/ecu/2/logs")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "cleared"


# ============================================================
# SOFTWARE UPDATES (OTA) - ASAM SOVD Section 6.6
# ============================================================

def test_get_updates_ecu2():
    """GET /ecu/2/updates - Catalogue OTA"""
    r = requests.get(f"{BASE_URL}/ecu/2/updates")
    assert r.status_code == 200
    data = r.json()
    assert "updates" in data
    assert data["total"] > 0

def test_install_update_upd_t001_ecu2():
    """POST /ecu/2/updates - Installer upd-t001"""
    payload = {"id": "upd-t001"}
    r = requests.post(f"{BASE_URL}/ecu/2/updates", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "upd-t001"
    assert data["status"] == "installing"

def test_update_status_upd_t001_ecu2():
    """GET /ecu/2/updates/upd-t001 - Statut OTA upd-t001"""
    r = requests.get(f"{BASE_URL}/ecu/2/updates/upd-t001")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "progress" in data

def test_install_update_upd_t002_ecu2():
    """POST /ecu/2/updates - Installer upd-t002"""
    payload = {"id": "upd-t002"}
    r = requests.post(f"{BASE_URL}/ecu/2/updates", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "upd-t002"
    assert data["status"] == "installing"

def test_update_status_upd_t002_ecu2():
    """GET /ecu/2/updates/upd-t002 - Statut OTA upd-t002"""
    r = requests.get(f"{BASE_URL}/ecu/2/updates/upd-t002")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "progress" in data

