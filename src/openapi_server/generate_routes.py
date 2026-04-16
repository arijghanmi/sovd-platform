# -*- coding: utf-8 -*-
# ============================================================
# generate_routes.py - Generateur Automatique de Routes SOVD
#
# Usage : python generate_routes.py
#
# Lit ecu1_config.yaml ET ecu2_config.yaml
# Genere les routes FastAPI pour les 2 ECUs :
#   ecu1_fault_handling_api.py  ecu2_fault_handling_api.py
#   ecu1_data_retrieval_api.py  ecu2_data_retrieval_api.py
#   ecu1_logging_api.py         ecu2_logging_api.py
#   ecu1_updates_api.py         ecu2_updates_api.py
#   ecu1_capabilities_api.py    ecu2_capabilities_api.py
#   ecu1_simulator.py           ecu2_simulator.py
#   discovery_api.py            (commun, retourne les 2 ECUs)
#   redis_init_multi.py         (initialisation Redis multi-ECU)
# ============================================================

import yaml, os, sys
from datetime import datetime

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "apis")
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

def header(name, ref, src):
    return f'''# coding: utf-8
# ============================================================
# {name}
# AUTO-GENERE par generate_routes.py - Source: {src}
# Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Reference ASAM SOVD V1.0.0 : {ref}
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

'''

# ============================================================
# FAULT HANDLING
# ============================================================
def generate_fault_handling(cfg, src, px):
    ecu  = cfg["ecu"]
    ec   = ecu["entity_collection"]
    eid  = ecu["entity_id"]
    fc   = ecu["faults"]
    rpfx = fc["redis_key_prefix"]
    cf   = fc["code_field"]
    df   = fc["dtc_field"]
    types= fc["types"]
    sp   = fc["scope_filter"]["param"]
    eva  = fc["log_events"]["add"]
    evc  = fc["log_events"]["clear"]

    pc           = fc.get("permanent_clear", {})
    perm_enabled = pc.get("enabled", False)
    perm_flag    = pc.get("redis_flag", f"ecu{eid}:driving_cycle_complete") if perm_enabled else ""

    return header(f"{px}_fault_handling_api.py", "Section faults", src) + f'''from typing import Any, Optional
import json
from fastapi import APIRouter, Body, HTTPException, Path, Query, Response
from openapi_server.shared import r, redis_add_log, redis_add_log_ecu

router = APIRouter()

_PREFIX    = "{rpfx}"
_CF        = "{cf}"
_DF        = "{df}"
_TYPES     = {types}
_EV_ADD    = "{eva}"
_EV_CLR    = "{evc}"
_EID       = "{eid}"
_PERM_FLAG = "{perm_flag}"

def _get_all(scope=None):
    faults = []
    for k in r.keys(f"{{_PREFIX}}:*"):
        raw = r.get(k)
        if raw:
            f = json.loads(raw)
            f["ecu_id"] = _EID
            faults.append(f)
    if scope:
        s = scope.upper()
        faults = [f for f in faults if f.get(_DF,"").upper() == s] if s in _TYPES else []
    return faults

def _get_by_id(fid):
    raw = r.get(f"{{_PREFIX}}:{{fid}}")
    if not raw: return None
    f = json.loads(raw)
    f["ecu_id"] = _EID
    return f

def _add(fault):
    code = fault.get(_CF, "UNKNOWN")
    t = fault.get(_DF, "ACTIVE").upper()
    fault[_DF] = t if t in _TYPES else _TYPES[0]
    fault["ecu_id"] = _EID
    r.set(f"{{_PREFIX}}:{{code}}", json.dumps(fault))
    return fault

def _delete_all(scope=None):
    deleted = 0
    cycle_done = _PERM_FLAG and r.get(_PERM_FLAG) == "true"
    for k in r.keys(f"{{_PREFIX}}:*"):
        try:
            f = json.loads(r.get(k))
            t = f.get(_DF,"ACTIVE").upper()
            if scope is None:
                if t in ["ACTIVE", "PENDING"]:
                    r.delete(k); deleted += 1
                elif t == "PERMANENT" and cycle_done:
                    r.delete(k); deleted += 1
            elif scope and scope.upper() == t:
                if t == "PERMANENT" and not cycle_done:
                    pass
                else:
                    r.delete(k); deleted += 1
        except: pass
    if cycle_done and _PERM_FLAG:
        r.delete(_PERM_FLAG)
    return deleted

def _count():
    c = {{t.lower(): 0 for t in _TYPES}}
    for k in r.keys(f"{{_PREFIX}}:*"):
        try:
            f = json.loads(r.get(k))
            t = f.get(_DF,"ACTIVE").lower()
            if t in c: c[t] += 1
        except: pass
    return c

def _cycle_status():
    if not _PERM_FLAG: return False
    return r.get(_PERM_FLAG) == "true"

@router.get("/{ec}/{eid}/faults", response_model=None, tags=["{px}-faults"], summary="ECU {eid} - Get Faults")
async def get_{px}_faults({sp}: Optional[str] = Query(None)):
    faults = _get_all(scope={sp})
    counts = _count()
    return {{
        "entity_id":"{eid}","ecu_id":"{eid}",
        "total_faults":sum(counts.values()),
        "faults":faults,"counts_by_type":counts,
        "permanent_clearable": _cycle_status()
    }}

@router.post("/{ec}/{eid}/faults", response_model=None, tags=["{px}-faults"], summary="ECU {eid} - Add Fault")
async def add_{px}_fault(body: Optional[Any] = Body(None)):
    if not body: raise HTTPException(400, "Body required")
    data = body if isinstance(body, dict) else body.dict()
    added = _add(data)
    redis_add_log_ecu(event=_EV_ADD, detail=f"ECU {eid} - Fault {{data.get(_CF,'?')}} injected", level="INFO", ecu_id="{eid}")
    return {{"message":"Fault added","fault":added}}

@router.delete("/{ec}/{eid}/faults", response_model=None, tags=["{px}-faults"], summary="ECU {eid} - Clear Faults")
async def clear_{px}_faults({sp}: Optional[str] = Query(None)):
    deleted = _delete_all(scope={sp})
    cycle_was_done = _cycle_status() if deleted == 0 else False
    redis_add_log_ecu(event=_EV_CLR, detail=f"ECU {eid} - Cleared {{deleted}} faults", level="INFO", ecu_id="{eid}")
    return {{
        "message":f"{{deleted}} fault(s) cleared",
        "ecu_id":"{eid}",
        "permanent_cleared": deleted > 0 and not cycle_was_done
    }}

@router.get("/{ec}/{eid}/faults/{{fid}}", response_model=None, tags=["{px}-faults"], summary="ECU {eid} - Get Fault By ID")
async def get_{px}_fault_by_id(fid: str = Path(...)):
    f = _get_by_id(fid)
    if not f: raise HTTPException(404, f"Fault '{{fid}}' not found in ECU {eid}")
    return {{"fault":f,"found":True}}
'''

# ============================================================
# DATA RETRIEVAL
# ============================================================
def generate_data_retrieval(cfg, src, px):
    ecu  = cfg["ecu"]
    ec   = ecu["entity_collection"]
    eid  = ecu["entity_id"]
    dc   = ecu["data"]
    rpfx = dc["redis_key_prefix"]
    sse  = dc["sse"]
    sdid = sse["data_id"]
    sev  = sse["event_name"]
    sint = sse["interval_ms"]
    smn  = sse["min_value"]
    smx  = sse["max_value"]
    sunit= sse["unit"]

    return header(f"{px}_data_retrieval_api.py", "Section data", src) + f'''from typing import Any, List, Optional
import asyncio, json, random, datetime
from fastapi import APIRouter, Body, HTTPException, Path, Query, Request, Response
from fastapi.responses import StreamingResponse
from openapi_server.shared import r

router = APIRouter()

_PREFIX = "{rpfx}"
_SDID   = "{sdid}"
_SEV    = "{sev}"
_SINT   = {sint} / 1000.0
_SMN    = {smn}
_SMX    = {smx}
_SUNIT  = "{sunit}"
_EID    = "{eid}"

def _get_all():
    items = []
    for k in r.keys(f"{{_PREFIX}}:*"):
        raw = r.get(k)
        if raw:
            it = json.loads(raw)
            it["ecu_id"] = _EID
            items.append(it)
    return items

def _get_by_id(did):
    raw = r.get(f"{{_PREFIX}}:{{did}}")
    if not raw: return None
    it = json.loads(raw)
    it["ecu_id"] = _EID
    return it

def _update(did, val):
    key = f"{{_PREFIX}}:{{did}}"
    raw = r.get(key)
    if not raw: return None
    it = json.loads(raw)
    it["value"] = val
    it["timestamp"] = datetime.datetime.utcnow().isoformat()+"Z"
    r.set(key, json.dumps(it))
    return it

@router.get("/{ec}/{eid}/data", response_model=None, tags=["{px}-data"], summary="ECU {eid} - Get All Data")
async def get_{px}_data():
    return _get_all()

@router.get("/{ec}/{eid}/data/{sdid}/events", response_model=None, tags=["{px}-data"], summary="ECU {eid} - SSE {sev}")
async def get_{px}_sse(request: Request):
    async def stream():
        try:
            yield 'event: connected\\ndata: {{"ecu_id":"{eid}","status":"subscribed"}}\\n\\n'
            while True:
                if await request.is_disconnected(): break
                try:
                    raw = r.get(f"{{_PREFIX}}:{{_SDID}}")
                    if raw:
                        v = json.loads(raw).get("value", 0)
                        if v in ["ff", "unavailable", None]:
                            val = "ff"
                        else:
                            val = round(float(v), 1)
                    else:
                        val = "ff"
                except:
                    val = "ff"
                payload = json.dumps({{"event":_SEV,"ecu_id":"{eid}","data":{{"id":_SDID,"value":val,"unit":_SUNIT if val != "ff" else "unavailable","timestamp":datetime.datetime.utcnow().isoformat()+"Z"}}}})
                yield f"event: {{_SEV}}\\ndata: {{payload}}\\n\\n"
                await asyncio.sleep(_SINT)
        except asyncio.CancelledError: pass
    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={{"Cache-Control":"no-cache","X-Accel-Buffering":"no","Connection":"keep-alive"}})

@router.get("/{ec}/{eid}/data/{sdid}", response_model=None, tags=["{px}-data"], summary="ECU {eid} - Get {sdid}")
async def get_{px}_{sdid}():
    try:
        raw = r.get(f"{{_PREFIX}}:{{_SDID}}")
        if raw:
            item = json.loads(raw)
            v = item.get("value", 0)
            if v in ["ff", "unavailable", None]:
                val = "ff"
                status = "simulator_offline"
            else:
                val = round(float(v), 1)
                status = "available"
        else:
            val = "ff"
            status = "simulator_offline"
    except:
        val = "ff"
        status = "simulator_offline"
    return {{"data_id":_SDID,"ecu_id":"{eid}","value":val,"unit":_SUNIT if val != "ff" else "unavailable","status":status,"timestamp":datetime.datetime.utcnow().isoformat()+"Z"}}

@router.get("/{ec}/{eid}/data/{{data_id}}", response_model=None, tags=["{px}-data"], summary="ECU {eid} - Get Data By ID")
async def get_{px}_data_by_id(data_id: str = Path(...)):
    it = _get_by_id(data_id)
    if not it: raise HTTPException(404, f"Data '{{data_id}}' not found in ECU {eid}")
    return it

@router.put("/{ec}/{eid}/data/{{data_id}}", response_model=None, tags=["{px}-data"], summary="ECU {eid} - Update Data")
async def update_{px}_data(data_id: str = Path(...), body: Optional[Any] = Body(None)):
    val = body.get("value") if isinstance(body, dict) else body
    res = _update(data_id, val)
    if not res: raise HTTPException(404, f"Data '{{data_id}}' not found in ECU {eid}")
    return {{"status":"updated","data_id":data_id,"ecu_id":"{eid}"}}
'''

# ============================================================
# LOGGING
# ============================================================
def generate_logging(cfg, src, px):
    ecu  = cfg["ecu"]
    ec   = ecu["entity_collection"]
    eid  = ecu["entity_id"]
    lc   = ecu["logs"]
    rkey = lc["redis_key"]
    lf   = lc["level_field"]
    mx   = lc["max_entries"]
    fp   = lc["filters"][0]["param"] if lc.get("filters") else "level"

    return header(f"{px}_logging_api.py", "Section logs", src) + f'''from typing import Optional
import json
from fastapi import APIRouter, Query, Response
from openapi_server.shared import r

router = APIRouter()

_RKEY = "{rkey}"
_LF   = "{lf}"
_MAX  = {mx}
_EID  = "{eid}"

def _get_logs(limit=100, level=None):
    entries = []
    for item in r.lrange(_RKEY, -limit, -1):
        try:
            e = json.loads(item)
            e["ecu_id"] = _EID
            entries.append(e)
        except: pass
    if level:
        entries = [e for e in entries if e.get(_LF,"").upper() == level.upper()]
    return list(reversed(entries))

@router.get("/{ec}/{eid}/logs", response_model=None, tags=["{px}-logs"], summary="ECU {eid} - Get Logs")
async def get_{px}_logs(limit: Optional[int] = Query({mx}), {fp}: Optional[str] = Query(None)):
    logs = _get_logs(limit=limit or _MAX, level={fp})
    return {{"entity_id":"{eid}","ecu_id":"{eid}","total":len(logs),"entries":logs}}

@router.delete("/{ec}/{eid}/logs", response_model=None, tags=["{px}-logs"], summary="ECU {eid} - Clear Logs")
async def clear_{px}_logs():
    r.delete(_RKEY)
    return {{"status":"cleared","ecu_id":"{eid}"}}
'''

# ============================================================
# UPDATES
# ============================================================
def generate_updates(cfg, src, px):
    ecu  = cfg["ecu"]
    ec   = ecu["entity_collection"]
    eid  = ecu["entity_id"]
    uc   = ecu["updates"]
    pcat = uc["redis_key_prefix_catalog"]
    psta = uc["redis_key_prefix_status"]
    idf  = uc["id_field"]
    stp  = uc["simulation"]["step_percent"]
    sdl  = uc["simulation"]["step_delay_seconds"]
    evs  = uc["log_events"]["start"]
    evc  = uc["log_events"]["complete"]

    return header(f"{px}_updates_api.py", "Section software-updates", src) + f'''from typing import Any, Optional
import json, threading, datetime
from fastapi import APIRouter, Body, HTTPException, Path, Response
from openapi_server.shared import r, redis_add_log

router = APIRouter()

_PCAT = "{pcat}"
_PSTA = "{psta}"
_IDF  = "{idf}"
_STP  = {stp}
_SDL  = {sdl}
_EVS  = "{evs}"
_EVC  = "{evc}"
_EID  = "{eid}"

def _catalog():
    items = []
    for k in r.keys(f"{{_PCAT}}:*"):
        raw = r.get(k)
        if raw:
            it = json.loads(raw)
            it["ecu_id"] = _EID
            items.append(it)
    return items

def _get_upd(uid):
    raw = r.get(f"{{_PCAT}}:{{uid}}")
    return json.loads(raw) if raw else None

def _get_sta(uid):
    raw = r.get(f"{{_PSTA}}:{{uid}}")
    return json.loads(raw) if raw else None

def _set_sta(uid, s):
    r.set(f"{{_PSTA}}:{{uid}}", json.dumps(s))

def _simulate(uid, ver):
    import time
    for p in range(_STP, 101, _STP):
        time.sleep(_SDL)
        _set_sta(uid, {{"id":uid,"version":ver,"ecu_id":_EID,"status":"installing","progress":p}})
    _set_sta(uid, {{"id":uid,"version":ver,"ecu_id":_EID,"status":"installed","progress":100}})
    redis_add_log(event=_EVC, detail=f"ECU {eid} - OTA {{uid}} ({{ver}}) installed", level="INFO")

@router.get("/{ec}/{eid}/updates", response_model=None, tags=["{px}-updates"], summary="ECU {eid} - Get Updates")
async def get_{px}_updates():
    return {{"entity_id":"{eid}","ecu_id":"{eid}","total":len(_catalog()),"updates":_catalog()}}

@router.post("/{ec}/{eid}/updates", response_model=None, tags=["{px}-updates"], summary="ECU {eid} - Install Update")
async def install_{px}_update(body: Optional[Any] = Body(None)):
    data = body if isinstance(body, dict) else {{}}
    uid = data.get(_IDF, "upd-001")
    upd = _get_upd(uid)
    if not upd: raise HTTPException(404, f"Update '{{uid}}' not found")
    _set_sta(uid, {{"id":uid,"version":upd["version"],"ecu_id":"{eid}","status":"installing","progress":0}})
    redis_add_log(event=_EVS, detail=f"ECU {eid} - OTA {{uid}} initiated", level="INFO")
    threading.Thread(target=_simulate, args=(uid, upd["version"]), daemon=True).start()
    return {{"id":uid,"version":upd["version"],"ecu_id":"{eid}","status":"installing","progress":0}}

@router.get("/{ec}/{eid}/updates/{{uid}}", response_model=None, tags=["{px}-updates"], summary="ECU {eid} - Update Status")
async def get_{px}_update_status(uid: str = Path(...)):
    s = _get_sta(uid)
    if not s: raise HTTPException(404, f"No update '{{uid}}' for ECU {eid}")
    return s
'''

# ============================================================
# CAPABILITIES
# ============================================================
def generate_capabilities(cfg, src, px):
    ecu  = cfg["ecu"]
    ec   = ecu["entity_collection"]
    eid  = ecu["entity_id"]
    desc = ecu["capabilities"]["description"]

    return header(f"{px}_capabilities_api.py", "Section capabilities", src) + f'''from typing import Optional
import yaml, json
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

_DESC = "{desc}"
_EID  = "{eid}"
_EC   = "{ec}"

def _load_openapi():
    with open("/home/pi/pfe1/sovd-server-fastapi-new/openapi.yaml","r") as f:
        spec = yaml.safe_load(f)
    return json.loads(json.dumps(spec, default=str))

def _ecu_capabilities():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu{eid}_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    ecu = cfg["ecu"]
    disc = ecu["discovery"]
    data_ids = [d["id"] for d in ecu["data"]["initial_data"]]
    resources = [r["name"] for r in disc["resources"]]
    endpoints = [f"GET /{ec}/{eid}/{{r}}".format() for r in resources]
    endpoints += [f"POST /{ec}/{eid}/faults",
                  f"DELETE /{ec}/{eid}/faults",
                  "PUT /ecu/{eid}/data/{{data_id}}"]
    return {{
        "title":           f"ECU {eid} Capability Description",
        "version":         "1.0.0",
        "description":     _DESC,
        "entity":          f"{ec}/{eid}",
        "ecu_id":          "{eid}",
        "name":            disc["name"],
        "resources":       resources,
        "data_ids":        data_ids,
        "endpoints":       endpoints,
        "endpoints_count": len(endpoints),
        "sovd_standard":   "ASAM SOVD V1.0.0",
        "mode":            "online",
        "config_source":   f"ecu{eid}_config.yaml"
    }}

@router.get("/{ec}/{eid}/docs", response_model=None, tags=["{px}-capabilities"], summary="ECU {eid} - Capabilities")
async def get_{px}_caps(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if include_schema:
        return JSONResponse(_load_openapi())
    return JSONResponse(_ecu_capabilities())

@router.get("/{ec}/{eid}/config", response_model=None, tags=["{px}-capabilities"], summary="ECU {eid} - Config YAML")
async def get_{px}_config():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu{eid}_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    return JSONResponse(cfg)
'''

# ============================================================
# DISCOVERY - commun aux 2 ECUs
# ============================================================
def generate_discovery(configs):
    ec = configs[0]["ecu"]["entity_collection"]
    ecus = []
    for cfg in configs:
        ecu  = cfg["ecu"]
        disc = ecu["discovery"]
        eid  = ecu["entity_id"]
        res  = {r["name"]: r["href"] for r in disc["resources"]}
        ecus.append({"eid": eid, "name": disc["name"], "desc": disc["description"], "res": res})

    items = ",\n    ".join([
        f'{{"id":"{e["eid"]}","name":"{e["name"]}","description":"{e["desc"]}","href":"/{ec}/{e["eid"]}"}}'
        for e in ecus
    ])

    concrete = ""
    for e in ecus:
        safe = e["eid"].replace("-","_")
        concrete += f'''
@router.get("/{ec}/{e["eid"]}", response_model=None, tags=["discovery"], summary="ECU {e["eid"]} Entity")
async def get_entity_{safe}(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    r = {{"id":"{e["eid"]}","name":"{e["name"]}","description":"{e["desc"]}","sovd_standard":"ASAM SOVD V1.0.0"}}
    r.update({e["res"]})
    return JSONResponse(r)
'''

    return f'''# coding: utf-8
# ============================================================
# discovery_api.py - Multi-ECU Discovery
# AUTO-GENERE par generate_routes.py
# Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# Reference ASAM SOVD V1.0.0 : Section 5.1 Discovery
# ============================================================

from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Query, Response
from fastapi.responses import JSONResponse

router = APIRouter()

_EC = "{ec}"
_RESERVED = {{"dashboard","health","components","swagger-ui","redoc","v3","areas","docs","openapi.json"}}

_ALL_ECUS = [
    {items}
]

@router.get("/{ec}", response_model=None, tags=["discovery"], summary="List All ECUs")
async def get_all_ecus(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    return JSONResponse({{"items": _ALL_ECUS}})

{concrete}

@router.get("/{{entity_collection}}/{{entity_id}}", response_model=None, tags=["discovery"])
async def entity_get(entity_collection: str = Path(...), entity_id: str = Path(...),
    include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if entity_collection in _RESERVED or entity_id in _RESERVED:
        raise HTTPException(404, "Not found")
    for ecu in _ALL_ECUS:
        if entity_collection == _EC and entity_id == ecu["id"]:
            return JSONResponse(ecu)
    return JSONResponse({{"id":entity_id,"entity_collection":entity_collection,"status":"multi-ECU environment"}})

@router.get("/{{entity_collection}}", response_model=None, tags=["discovery"])
async def collection_get(entity_collection: str = Path(...),
    include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if entity_collection in _RESERVED:
        raise HTTPException(404, "Not a SOVD entity collection")
    if entity_collection == _EC:
        return JSONResponse({{"items": _ALL_ECUS}})
    return JSONResponse({{"items": []}})

@router.get("/areas/{{aid}}/subareas", response_model=None, tags=["discovery"])
async def areas_sub(aid: str = Path(...)): return Response(status_code=501)

@router.get("/components/{{cid}}/subcomponents", response_model=None, tags=["discovery"])
async def components_sub(cid: str = Path(...)): return Response(status_code=501)
'''

# ============================================================
# REDIS INIT MULTI-ECU
# ============================================================
def generate_redis_init(configs):
    code = f'''# coding: utf-8
# ============================================================
# redis_init_multi.py - Initialisation Redis Multi-ECU
# AUTO-GENERE - Date: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
# ============================================================

import redis, json
r = redis.Redis(host="localhost", port=6379, decode_responses=True)

def redis_init_all_ecus():
'''
    for cfg in configs:
        ecu = cfg["ecu"]
        eid = ecu["entity_id"]

        dp = ecu["data"]["redis_key_prefix"]
        code += f'''
    # ECU {eid} - Data
    for item in {ecu["data"]["initial_data"]}:
        k = f"{dp}:{{item['id']}}"
        if not r.exists(k): r.set(k, json.dumps(item))
'''
        up = ecu["updates"]["redis_key_prefix_catalog"]
        code += f'''
    # ECU {eid} - Updates
    for upd in {ecu["updates"]["initial_catalog"]}:
        k = f"{up}:{{upd['id']}}"
        if not r.exists(k): r.set(k, json.dumps(upd))
'''

    code += '''
redis_init_all_ecus()
print("[Redis] Multi-ECU init complete (ECU1 + ECU2)")
'''
    return code

# ============================================================
# SIMULATOR - Approche A (steps synchronises)
# ============================================================
def generate_simulator(cfg, src, px):
    ecu      = cfg["ecu"]
    eid      = ecu["entity_id"]
    dpfx     = ecu["data"]["redis_key_prefix"]
    sim      = ecu["data"].get("simulation", {})
    mode     = sim.get("mode", "random")
    loop     = sim.get("loop", True)
    interval = sim.get("interval_ms", 500)
    scenario = sim.get("scenario", [])

    data_ids = [k for k in scenario[0].keys() if k != "duration"] if scenario else []

    return header(f"{px}_simulator.py", "Section data / simulation", src) + f'''import redis, json, time, datetime, itertools

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

_PREFIX   = "{dpfx}"
_EID      = "{eid}"
_LOOP     = {loop}
_INTERVAL = {interval} / 1000.0
_DATA_IDS = {data_ids}
_SCENARIO = {scenario}

def write_value(data_id, value):
    key = f"{{_PREFIX}}:{{data_id}}"
    raw = r.get(key)
    if raw:
        item = json.loads(raw)
    else:
        # Lire les metadata depuis initial_data du YAML
        _meta = {{d["id"]: d for d in {ecu["data"]["initial_data"]}}}
        meta = _meta.get(data_id, {{}})
        item = {{
            "id": data_id,
            "unit": meta.get("unit", ""),
            "quality": meta.get("quality", "good"),
            "description": meta.get("description", data_id)
        }}
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
        r.set(f"ecu{{_EID}}:simulator:status", "online")
        elapsed = 0.0
        while elapsed < duration:
            time.sleep(_INTERVAL)
            elapsed += _INTERVAL

if __name__ == "__main__":
    print(f"[ECU {{_EID}} Simulator] scenario mode - {{len(_SCENARIO)}} steps, loop={{_LOOP}}")
    try:
        run_scenario()
    except KeyboardInterrupt:
        r.set(f"ecu{{_EID}}:simulator:status", "offline")
        print(f"[ECU {{_EID}} Simulator] Stopped")
'''

# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    print("=" * 60)
    print("  SOVD Multi-ECU Route Generator")
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
        px  = f"ecu{eid}"
        write_file(f"{px}_fault_handling_api.py", generate_fault_handling(cfg, src, px))
        write_file(f"{px}_data_retrieval_api.py", generate_data_retrieval(cfg, src, px))
        write_file(f"{px}_logging_api.py",        generate_logging(cfg, src, px))
        write_file(f"{px}_updates_api.py",        generate_updates(cfg, src, px))
        write_file(f"{px}_capabilities_api.py",   generate_capabilities(cfg, src, px))
        write_file(f"{px}_simulator.py",          generate_simulator(cfg, src, px))
        print()

    write_file("discovery_api.py",    generate_discovery([c for c,_ in configs]))
    write_file("redis_init_multi.py", generate_redis_init([c for c,_ in configs]))

    print()
    print("  DONE - 13 fichiers generes pour 2 ECUs (+ 2 simulateurs)")
    print()
    print("  Mettre a jour main.py - ajouter ces imports:")
    for cfg, _ in configs:
        eid = cfg["ecu"]["entity_id"]
        px  = f"ecu{eid}"
        print(f"  from openapi_server.apis.{px}_fault_handling_api import router as {px}_fault_router")
        print(f"  from openapi_server.apis.{px}_data_retrieval_api import router as {px}_data_router")
        print(f"  from openapi_server.apis.{px}_logging_api import router as {px}_log_router")
        print(f"  from openapi_server.apis.{px}_updates_api import router as {px}_upd_router")
        print(f"  from openapi_server.apis.{px}_capabilities_api import router as {px}_cap_router")
        print()
    print("  Et enregistrer tous les routers dans app.include_router(...)")
    print("=" * 60)