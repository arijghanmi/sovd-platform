# coding: utf-8
# ============================================================
# ecu2_simulator.py
# AUTO-GENERE par generate_routes.py - Source: ecu2_config.yaml
# Date: 2026-04-15 15:26:21
# Reference ASAM SOVD V1.0.0 : Section data / simulation
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

import redis, json, time, datetime, itertools

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

_PREFIX   = "ecu2:data"
_EID      = "2"
_LOOP     = True
_INTERVAL = 500 / 1000.0
_DATA_IDS = ['gear', 'oil_temp', 'oil_pressure', 'torque', 'efficiency']
_SCENARIO = [{'duration': 2, 'gear': 1, 'oil_temp': 60.0, 'oil_pressure': 2.5, 'torque': 150.0, 'efficiency': 85.0}, {'duration': 2, 'gear': 2, 'oil_temp': 65.0, 'oil_pressure': 2.8, 'torque': 200.0, 'efficiency': 88.0}, {'duration': 2, 'gear': 3, 'oil_temp': 70.0, 'oil_pressure': 3.0, 'torque': 240.0, 'efficiency': 91.0}, {'duration': 3, 'gear': 4, 'oil_temp': 75.0, 'oil_pressure': 3.2, 'torque': 270.0, 'efficiency': 93.0}]

def write_value(data_id, value):
    key = f"{_PREFIX}:{data_id}"
    raw = r.get(key)
    if raw:
        item = json.loads(raw)
    else:
        # Lire les metadata depuis initial_data du YAML
        _meta = {d["id"]: d for d in [{'id': 'gear', 'value': 1, 'unit': '', 'quality': 'good', 'description': 'Current gear'}, {'id': 'oil_temp', 'value': 60.0, 'unit': 'C', 'quality': 'good', 'description': 'Transmission oil temperature'}, {'id': 'oil_pressure', 'value': 2.5, 'unit': 'bar', 'quality': 'good', 'description': 'Transmission oil pressure'}, {'id': 'torque', 'value': 150.0, 'unit': 'Nm', 'quality': 'good', 'description': 'Engine torque'}, {'id': 'efficiency', 'value': 85.0, 'unit': '%', 'quality': 'good', 'description': 'Transmission efficiency'}]}
        meta = _meta.get(data_id, {})
        item = {
            "id": data_id,
            "unit": meta.get("unit", ""),
            "quality": meta.get("quality", "good"),
            "description": meta.get("description", data_id)
        }
    item["value"] = value
    item["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    r.set(key, json.dumps(item))

def run_scenario():
    steps = itertools.cycle(_SCENARIO) if _LOOP else iter(_SCENARIO)
    for step in steps:
        duration = step.get("duration", 1)
        for data_id in _DATA_IDS:
            if data_id in step:
                write_value(data_id, step[data_id])
        r.set(f"ecu{_EID}:simulator:status", "online")
        elapsed = 0.0
        while elapsed < duration:
            time.sleep(_INTERVAL)
            elapsed += _INTERVAL

if __name__ == "__main__":
    print(f"[ECU {_EID} Simulator] scenario mode - {len(_SCENARIO)} steps, loop={_LOOP}")
    try:
        run_scenario()
    except KeyboardInterrupt:
        r.set(f"ecu{_EID}:simulator:status", "offline")
        print(f"[ECU {_EID} Simulator] Stopped")
