# Shared storage - Redis remplace le dictionnaire RAM
# Analogie AUTOSAR : ara::per::KeyValueStorage
import redis
import json

# Connexion Redis locale
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# ============================================================
# FONCTIONS REDIS - FAULT HANDLING
# equivalents ara::per::KeyValueStorage
# ============================================================

def redis_set_fault(fault: dict):
    """
    Equivalent ara::per::KeyValueStorage::SetValue
    Cle unique par code DTC -> gestion automatique des doublons
    """
    code = fault.get("faultCode") or fault.get("dtc_code", "UNKNOWN")
    key = f"fault:{code}"
    r.set(key, json.dumps(fault))

def redis_get_all() -> dict:
    """
    Equivalent ara::per::KeyValueStorage::GetAllKeys + GetValue
    Reconstruit le fault_memory depuis Redis
    """
    active = []
    pending = []
    permanent = []
    keys = r.keys("fault:*")
    for k in keys:
        try:
            f = json.loads(r.get(k))
            t = f.get("dtc_type", "ACTIVE").upper()
            if t == "PERMANENT":
                permanent.append(f)
            elif t == "PENDING":
                pending.append(f)
            else:
                active.append(f)
        except Exception:
            pass
    return {
        "active_faults": active,
        "pending_faults": pending,
        "permanent_faults": permanent
    }

def redis_clear_faults(scope=None):
    """
    Equivalent ara::per::KeyValueStorage::ResetKeyValueStorage
    scope=None      -> efface actifs + pendants
    scope=permanent -> efface uniquement permanents
    """
    keys = r.keys("fault:*")
    for k in keys:
        try:
            f = json.loads(r.get(k))
            t = f.get("dtc_type", "ACTIVE").upper()
            if scope == "permanent" and t == "PERMANENT":
                r.delete(k)
            elif scope is None and t != "PERMANENT":
                r.delete(k)
        except Exception:
            pass

def redis_count() -> dict:
    """Retourne le nombre de DTCs par type"""
    fm = redis_get_all()
    return {
        "active": len(fm["active_faults"]),
        "pending": len(fm["pending_faults"]),
        "permanent": len(fm["permanent_faults"])
    }

# ============================================================
# PROXY DE COMPATIBILITE
# Permet a faults.py d utiliser fault_memory comme avant
# sans changer son code
# ============================================================
class RedisProxy:
    """
    Proxy transparent : rend Redis compatible avec
    l interface dictionnaire de l ancien fault_memory
    """
    def __getitem__(self, key):
        return redis_get_all()[key]

    def __setitem__(self, key, value):
        pass  # les ecritures passent par redis_set_fault

    def get(self, key, default=None):
        return redis_get_all().get(key, default)

# fault_memory est maintenant un proxy Redis
fault_memory = RedisProxy()

# ============================================================
# FONCTIONS REDIS - DATA RETRIEVAL (Use Case 1)
# Equivalent ara::per::KeyValueStorage pour les donnees ECU
# ============================================================

_INITIAL_DATA = {
    "speed":       {"id": "speed",       "value": 0,    "unit": "km/h", "quality": "good", "description": "Vehicle speed"},
    "rpm":         {"id": "rpm",         "value": 800,  "unit": "rpm",  "quality": "good", "description": "Engine RPM"},
    "fuel_level":  {"id": "fuel_level",  "value": 65.0, "unit": "%",    "quality": "good", "description": "Fuel level"},
    "temperature": {"id": "temperature", "value": 90.0, "unit": "C",    "quality": "good", "description": "Coolant temperature"},
    "voltage":     {"id": "voltage",     "value": 12.6, "unit": "V",    "quality": "good", "description": "Battery voltage"},
}

def redis_init_data():
    """
    Initialise les donnees ECU dans Redis au premier demarrage.
    Equivalent ara::per::KeyValueStorage initialisation.
    Idempotent : n ecrase pas les valeurs existantes.
    """
    for did, val in _INITIAL_DATA.items():
        key = f"data:{did}"
        if not r.exists(key):
            r.set(key, json.dumps(val))

def redis_get_all_data() -> list:
    """
    Retourne tous les items de donnees ECU depuis Redis.
    Equivalent ara::per::KeyValueStorage GetAllKeys + GetValue.
    """
    keys = r.keys("data:*")
    items = []
    for k in keys:
        try:
            items.append(json.loads(r.get(k)))
        except Exception:
            pass
    return items

def redis_get_data_by_id(did: str):
    """
    Retourne un item de donnee par son identifiant depuis Redis.
    Equivalent ara::per::KeyValueStorage GetValue.
    Retourne None si l item n existe pas.
    """
    raw = r.get(f"data:{did}")
    if not raw:
        return None
    return json.loads(raw)

def redis_update_data(did: str, new_value):
    """
    Met a jour la valeur d un item de donnee dans Redis.
    Equivalent ara::per::KeyValueStorage SetValue.
    Retourne None si l item n existe pas.
    """
    import datetime
    key = f"data:{did}"
    raw = r.get(key)
    if not raw:
        return None
    item = json.loads(raw)
    item["value"] = new_value
    item["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    r.set(key, json.dumps(item))
    return item

# Initialisation automatique au chargement du module
redis_init_data()

# ============================================================
# FONCTIONS REDIS - LOGGING (Use Case 2)
# Equivalent ara::per::KeyValueStorage pour les logs diagnostics
# ============================================================

def redis_add_log(event: str, detail: str, level: str = "INFO"):
    """
    Ajoute une entree de log dans Redis.
    Appele automatiquement a chaque fault detecte ou efface.
    Equivalent ara::per::KeyValueStorage SetValue pour les logs.
    """
    import time as _time
    import datetime as _dt
    log = {
        "id":        f"log-{int(_time.time() * 1000)}",
        "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
        "level":     level,
        "event":     event,
        "detail":    detail,
        "source":    "sovd-engine-ecu"
    }
    r.rpush("logs:entries", json.dumps(log))
    r.ltrim("logs:entries", -200, -1)

def redis_get_logs(limit: int = 100) -> list:
    """
    Retourne les dernieres entrees de log depuis Redis.
    Equivalent ara::per::KeyValueStorage GetAllKeys + GetValue.
    """
    raw = r.lrange("logs:entries", -limit, -1)
    entries = []
    for item in raw:
        try:
            entries.append(json.loads(item))
        except Exception:
            pass
    return list(reversed(entries))

def redis_clear_logs():
    """Efface tous les logs Redis."""
    r.delete("logs:entries")

# ============================================================
# FONCTIONS REDIS - SOFTWARE UPDATES (Use Case 3)
# Equivalent ara::per::KeyValueStorage pour les mises a jour OTA
# Meme pattern que redis_set_fault / redis_get_all
# ============================================================

_UPDATES_CATALOG = [
    {
        "id":          "upd-001",
        "version":     "v2.1.3",
        "description": "Engine ECU firmware — stability improvements and sensor calibration",
        "size_mb":     12.4,
        "status":      "available",
        "released_at": "2026-03-15",
        "critical":    False
    },
    {
        "id":          "upd-002",
        "version":     "v2.2.0-security",
        "description": "Security patch 2026-04 — CAN bus authentication hardening",
        "size_mb":     4.1,
        "status":      "available",
        "released_at": "2026-04-01",
        "critical":    True
    }
]

def redis_init_updates():
    """
    Initialise le catalogue des mises a jour dans Redis.
    Equivalent ara::per::KeyValueStorage initialisation OTA.
    Idempotent — n ecrase pas les entrees existantes.
    """
    for upd in _UPDATES_CATALOG:
        key = f"update:catalog:{upd['id']}"
        if not r.exists(key):
            r.set(key, json.dumps(upd))

def redis_get_updates() -> list:
    """
    Retourne la liste des mises a jour disponibles depuis Redis.
    Equivalent ara::per::KeyValueStorage GetAllKeys pour les updates.
    """
    keys = r.keys("update:catalog:*")
    items = []
    for k in keys:
        try:
            items.append(json.loads(r.get(k)))
        except Exception:
            pass
    return items

def redis_get_update_status(uid: str):
    """
    Retourne le statut d une mise a jour en cours.
    Equivalent ara::per::KeyValueStorage GetValue pour le statut.
    Retourne None si aucune installation en cours.
    """
    raw = r.get(f"update:status:{uid}")
    if not raw:
        return None
    return json.loads(raw)

def redis_set_update_status(uid: str, status: dict):
    """
    Met a jour le statut d une installation dans Redis.
    Equivalent ara::per::KeyValueStorage SetValue.
    """
    r.set(f"update:status:{uid}", json.dumps(status))

# Initialisation automatique au chargement du module
redis_init_updates()


def redis_add_log_ecu(event: str, detail: str, level: str = "INFO", ecu_id: str = "1"):
    import time as _time
    import datetime as _dt
    log = {
        "id":        f"log-{int(_time.time() * 1000)}",
        "timestamp": _dt.datetime.utcnow().isoformat() + "Z",
        "level":     level,
        "event":     event,
        "detail":    detail,
        "source":    f"sovd-ecu{ecu_id}",
        "ecu_id":    ecu_id
    }
    key = f"ecu{ecu_id}:logs:entries"
    r.rpush(key, json.dumps(log))
    r.ltrim(key, -200, -1)
