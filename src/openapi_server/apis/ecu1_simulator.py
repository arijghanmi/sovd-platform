# coding: utf-8
# ============================================================
# ecu1_simulator.py
# AUTO-GENERE par generate_routes.py - Source: ecu1_config.yaml
# Date: 2026-04-16 14:59:27
# Reference ASAM SOVD V1.0.0 : Section data / simulation
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

import redis, json, time, datetime, itertools

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

_PREFIX   = "ecu1:data"
_EID      = "1"
_LOOP     = True
_INTERVAL = 500 / 1000.0
_DATA_IDS = ['speed', 'rpm', 'fuel_level', 'temperature', 'voltage']
_SCENARIO = [{'duration': 2, 'speed': 0, 'rpm': 800, 'fuel_level': 65.0, 'temperature': 85.0, 'voltage': 12.6}, {'duration': 2, 'speed': 50, 'rpm': 2500, 'fuel_level': 64.8, 'temperature': 88.0, 'voltage': 12.5}, {'duration': 2, 'speed': 70, 'rpm': 3200, 'fuel_level': 64.5, 'temperature': 91.0, 'voltage': 12.4}, {'duration': 3, 'speed': 90, 'rpm': 4000, 'fuel_level': 64.0, 'temperature': 95.0, 'voltage': 12.3}]

def write_value(data_id, value):
    key = f"{_PREFIX}:{data_id}"
    raw = r.get(key)
    if raw:
        item = json.loads(raw)
    else:
        # Lire les metadata depuis initial_data du YAML
        _meta = {d["id"]: d for d in [{'id': 'speed', 'value': 0, 'unit': 'km/h', 'quality': 'good', 'description': 'Vehicle speed'}, {'id': 'rpm', 'value': 800, 'unit': 'rpm', 'quality': 'good', 'description': 'Engine RPM'}, {'id': 'fuel_level', 'value': 65.0, 'unit': '%', 'quality': 'good', 'description': 'Fuel level'}, {'id': 'temperature', 'value': 90.0, 'unit': 'C', 'quality': 'good', 'description': 'Coolant temperature'}, {'id': 'voltage', 'value': 12.6, 'unit': 'V', 'quality': 'good', 'description': 'Battery voltage'}]}
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
        r.set(f"ecu{_EID}:simulator:last_seen", datetime.datetime.utcnow().isoformat())
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
