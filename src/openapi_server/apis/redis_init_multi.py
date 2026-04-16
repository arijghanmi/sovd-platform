# coding: utf-8
# ============================================================
# redis_init_multi.py - Initialisation Redis Multi-ECU
# AUTO-GENERE - Date: 2026-04-15 15:26:21
# ============================================================

import redis, json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def redis_init_all_ecus():

    # ECU 1 - Data
    for item in [{'id': 'speed', 'value': 0, 'unit': 'km/h', 'quality': 'good', 'description': 'Vehicle speed'}, {'id': 'rpm', 'value': 800, 'unit': 'rpm', 'quality': 'good', 'description': 'Engine RPM'}, {'id': 'fuel_level', 'value': 65.0, 'unit': '%', 'quality': 'good', 'description': 'Fuel level'}, {'id': 'temperature', 'value': 90.0, 'unit': 'C', 'quality': 'good', 'description': 'Coolant temperature'}, {'id': 'voltage', 'value': 12.6, 'unit': 'V', 'quality': 'good', 'description': 'Battery voltage'}]:
        k = f"ecu1:data:{item['id']}"
        if not r.exists(k): r.set(k, json.dumps(item))

    # ECU 1 - Updates
    for upd in [{'id': 'upd-001', 'version': 'v2.1.3', 'description': 'Engine ECU firmware — stability improvements and sensor calibration', 'size_mb': 12.4, 'status': 'available', 'released_at': '2026-03-15', 'critical': False}, {'id': 'upd-002', 'version': 'v2.2.0-security', 'description': 'Security patch 2026-04 — CAN bus authentication hardening', 'size_mb': 4.1, 'status': 'available', 'released_at': '2026-04-01', 'critical': True}]:
        k = f"ecu1:update:catalog:{upd['id']}"
        if not r.exists(k): r.set(k, json.dumps(upd))

    # ECU 2 - Data
    for item in [{'id': 'gear', 'value': 1, 'unit': '', 'quality': 'good', 'description': 'Current gear'}, {'id': 'oil_temp', 'value': 60.0, 'unit': 'C', 'quality': 'good', 'description': 'Transmission oil temperature'}, {'id': 'oil_pressure', 'value': 2.5, 'unit': 'bar', 'quality': 'good', 'description': 'Transmission oil pressure'}, {'id': 'torque', 'value': 150.0, 'unit': 'Nm', 'quality': 'good', 'description': 'Engine torque'}, {'id': 'efficiency', 'value': 85.0, 'unit': '%', 'quality': 'good', 'description': 'Transmission efficiency'}]:
        k = f"ecu2:data:{item['id']}"
        if not r.exists(k): r.set(k, json.dumps(item))

    # ECU 2 - Updates
    for upd in [{'id': 'upd-t001', 'version': 'v1.4.2', 'description': 'Transmission ECU firmware — gear shift optimization', 'size_mb': 8.2, 'status': 'available', 'released_at': '2026-03-20', 'critical': False}, {'id': 'upd-t002', 'version': 'v1.5.0-critical', 'description': 'Critical fix — torque limiter safety patch', 'size_mb': 3.1, 'status': 'available', 'released_at': '2026-04-05', 'critical': True}]:
        k = f"ecu2:update:catalog:{upd['id']}"
        if not r.exists(k): r.set(k, json.dumps(upd))

redis_init_all_ecus()
print("[Redis] Multi-ECU init complete (ECU1 + ECU2)")
