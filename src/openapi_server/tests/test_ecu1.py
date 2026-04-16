# -*- coding: utf-8 -*-
# ============================================================
# test_ecu1.py
# AUTO-GENERE par generate_tests.py - Source: ecu1_config.yaml
# Date: 2026-04-15 16:25:31
# Reference ASAM SOVD V1.0.0
# NE PAS MODIFIER MANUELLEMENT
# Execution : pytest test_ecu1.py -v
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
    assert "1" in ids

def test_discovery_ecu1_entity():
    """GET /ecu/1 - Entite ECU 1"""
    r = requests.get(f"{BASE_URL}/ecu/1")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "1"


# ============================================================
# CAPABILITIES - ASAM SOVD Section 5.2
# ============================================================

def test_capabilities_ecu1():
    """GET /ecu/1/docs - Capability description"""
    r = requests.get(f"{BASE_URL}/ecu/1/docs")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu_id"] == "1"
    assert "resources" in data
    assert "data_ids" in data
    assert data["sovd_standard"] == "ASAM SOVD V1.0.0"

def test_capabilities_ecu1_include_schema():
    """GET /ecu/1/docs?include-schema=true - OpenAPI schema"""
    r = requests.get(f"{BASE_URL}/ecu/1/docs", params={"include-schema": "true"})
    assert r.status_code == 200

def test_config_ecu1():
    """GET /ecu/1/config - Config YAML source of truth"""
    r = requests.get(f"{BASE_URL}/ecu/1/config")
    assert r.status_code == 200
    data = r.json()
    assert data["ecu"]["entity_id"] == "1"


# ============================================================
# FAULT HANDLING - ASAM SOVD Section 6.3
# ============================================================

def test_get_faults_ecu1():
    """GET /ecu/1/faults - Liste les faults"""
    r = requests.get(f"{BASE_URL}/ecu/1/faults")
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data
    assert "total_faults" in data
    assert "counts_by_type" in data

def test_get_faults_ecu1_scope_active():
    """GET /ecu/1/faults?scope=ACTIVE - Filtre par type ACTIVE"""
    r = requests.get(f"{BASE_URL}/ecu/1/faults", params={"scope": "ACTIVE"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_get_faults_ecu1_scope_pending():
    """GET /ecu/1/faults?scope=PENDING - Filtre par type PENDING"""
    r = requests.get(f"{BASE_URL}/ecu/1/faults", params={"scope": "PENDING"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_get_faults_ecu1_scope_permanent():
    """GET /ecu/1/faults?scope=PERMANENT - Filtre par type PERMANENT"""
    r = requests.get(f"{BASE_URL}/ecu/1/faults", params={"scope": "PERMANENT"})
    assert r.status_code == 200
    data = r.json()
    assert "faults" in data

def test_add_fault_ecu1():
    """POST /ecu/1/faults - Injection DTC"""
    payload = {
        "faultCode": "TEST001",
        "description": "Test fault injected by pytest",
        "severity": 1,
        "component": "test",
        "dtc_type": "ACTIVE"
    }
    r = requests.post(f"{BASE_URL}/ecu/1/faults", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "fault" in data

def test_get_fault_by_id_ecu1():
    """GET /ecu/1/faults/TEST001 - Fault par ID"""
    r = requests.get(f"{BASE_URL}/ecu/1/faults/TEST001")
    assert r.status_code == 200
    data = r.json()
    assert data["found"] == True

def test_clear_faults_ecu1():
    """DELETE /ecu/1/faults - Suppression faults"""
    r = requests.delete(f"{BASE_URL}/ecu/1/faults")
    assert r.status_code == 200
    data = r.json()
    assert "cleared" in data["message"]


# ============================================================
# DATA RETRIEVAL - ASAM SOVD Section 6.1
# ============================================================

def test_get_all_data_ecu1():
    """GET /ecu/1/data - Tous les data items"""
    r = requests.get(f"{BASE_URL}/ecu/1/data")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_data_speed_ecu1():
    """GET /ecu/1/data/speed - Valeur speed"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/speed")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_rpm_ecu1():
    """GET /ecu/1/data/rpm - Valeur rpm"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/rpm")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_fuel_level_ecu1():
    """GET /ecu/1/data/fuel_level - Valeur fuel_level"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/fuel_level")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_temperature_ecu1():
    """GET /ecu/1/data/temperature - Valeur temperature"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/temperature")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_get_data_voltage_ecu1():
    """GET /ecu/1/data/voltage - Valeur voltage"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/voltage")
    assert r.status_code == 200
    data = r.json()
    assert "value" in data or data.get("value") == "ff"

def test_update_data_ecu1():
    """PUT /ecu/1/data/speed - Mise a jour valeur"""
    payload = {"value": 42}
    r = requests.put(f"{BASE_URL}/ecu/1/data/speed", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "updated"

def test_get_data_invalid_id_ecu1():
    """GET /ecu/1/data/nonexistent - ID inexistant retourne 404"""
    r = requests.get(f"{BASE_URL}/ecu/1/data/nonexistent_data_id_xyz")
    assert r.status_code == 404


# ============================================================
# SSE (ResponseOnEvent) - ASAM SOVD Section 6.5
# ============================================================

def test_sse_endpoint_ecu1_exists():
    """GET /ecu/1/data/speed/events - SSE endpoint accessible"""
    import threading, time
    result = {}
    def fetch():
        try:
            r = requests.get(
                f"{BASE_URL}/ecu/1/data/speed/events",
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

def test_get_logs_ecu1():
    """GET /ecu/1/logs - Liste les logs"""
    r = requests.get(f"{BASE_URL}/ecu/1/logs")
    assert r.status_code == 200
    data = r.json()
    assert "entries" in data
    assert "total" in data

def test_get_logs_with_limit_ecu1():
    """GET /ecu/1/logs?limit=5 - Limite les logs"""
    r = requests.get(f"{BASE_URL}/ecu/1/logs", params={"limit": 5})
    assert r.status_code == 200
    data = r.json()
    assert len(data["entries"]) <= 5

def test_clear_logs_ecu1():
    """DELETE /ecu/1/logs - Suppression logs"""
    r = requests.delete(f"{BASE_URL}/ecu/1/logs")
    assert r.status_code == 200
    data = r.json()
    assert data["status"] == "cleared"


# ============================================================
# SOFTWARE UPDATES (OTA) - ASAM SOVD Section 6.6
# ============================================================

def test_get_updates_ecu1():
    """GET /ecu/1/updates - Catalogue OTA"""
    r = requests.get(f"{BASE_URL}/ecu/1/updates")
    assert r.status_code == 200
    data = r.json()
    assert "updates" in data
    assert data["total"] > 0

def test_install_update_upd_001_ecu1():
    """POST /ecu/1/updates - Installer upd-001"""
    payload = {"id": "upd-001"}
    r = requests.post(f"{BASE_URL}/ecu/1/updates", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "upd-001"
    assert data["status"] == "installing"

def test_update_status_upd_001_ecu1():
    """GET /ecu/1/updates/upd-001 - Statut OTA upd-001"""
    r = requests.get(f"{BASE_URL}/ecu/1/updates/upd-001")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "progress" in data

def test_install_update_upd_002_ecu1():
    """POST /ecu/1/updates - Installer upd-002"""
    payload = {"id": "upd-002"}
    r = requests.post(f"{BASE_URL}/ecu/1/updates", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == "upd-002"
    assert data["status"] == "installing"

def test_update_status_upd_002_ecu1():
    """GET /ecu/1/updates/upd-002 - Statut OTA upd-002"""
    r = requests.get(f"{BASE_URL}/ecu/1/updates/upd-002")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "progress" in data

