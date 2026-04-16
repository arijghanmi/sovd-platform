import json
import random
import time
import requests

# ============================================================
# SOVD Raspberry Button Client
# Projet : sovd-server-fastapi-new
# Endpoint : POST /ecu/engine/faults
# Double ENTER = injection DTC aleatoire
# ============================================================

import yaml
with open("raspberry_button_config.yaml", "r") as f:
    config = yaml.safe_load(f)

BASE_URL = config["sovd"]["base_url"]
DB_PATH  = config["dtc_database_path"]

with open(DB_PATH, "r") as f:
    dtc_database = json.load(f)["dtcs"]

print("=" * 50)
print("  SOVD Raspberry Button Client")
print(f"  Endpoint : {BASE_URL}/ecu/1|2/faults")
print(f"  DTCs disponibles : {len(dtc_database)}")
print("  Double ENTER pour injecter un DTC")
print("=" * 50)
ecu_toggle = [1]  # utiliser liste pour modifier dans closure

def send_random_dtc():
    from datetime import datetime
    dtc_raw = random.choice(dtc_database)
    
    # Alterner entre ECU 1 et ECU 2
    ecu_id = ecu_toggle[0]
    ecu_toggle[0] = 2 if ecu_toggle[0] == 1 else 1
    
    url = f"{BASE_URL}/ecu/{ecu_id}/faults"
    
    dtc = {
        "faultCode":   dtc_raw["faultCode"],
        "description": dtc_raw["description"],
        "severity":    dtc_raw["severity"],
        "component":   dtc_raw.get("component", "engine"),
        "source":      f"ecu{ecu_id}-simulator",
        "dtc_type":    "PERMANENT" if dtc_raw.get("isPermanent") else "ACTIVE",
        "timestamp":   datetime.utcnow().strftime("%H:%M:%S")
    }
    try:
        response = requests.post(url, json=dtc, timeout=3)
        status = response.status_code
    except Exception as e:
        status = f"ERROR: {e}"
    
    print(f"\n[DTC INJECTE → ECU {ecu_id}]")
    print(f"  Code      : {dtc['faultCode']}")
    print(f"  Desc      : {dtc['description']}")
    print(f"  Type      : {dtc['dtc_type']}")
    print(f"  Severity  : {dtc['severity']}")
    print(f"  Component : {dtc['component']}")
    print(f"  URL       : {url}")
    print(f"  Status    : {status}")
    print("-" * 50)

last_press = 0
DOUBLE_PRESS_DELAY = 1.0

try:
    while True:
        input()
        current_time = time.time()
        if current_time - last_press < DOUBLE_PRESS_DELAY:
            print("Double appui detecte !")
            send_random_dtc()
            last_press = 0
        else:
            print("Premier appui... appuyez encore une fois rapidement !")
            last_press = current_time
except KeyboardInterrupt:
    print("\n[SOVD Button] Arret")
