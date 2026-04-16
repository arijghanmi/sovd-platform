# coding: utf-8
# ============================================================
# ecu2_updates_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu2_config.yaml
# Date: 2026-04-15 15:26:21
# Reference ASAM SOVD V1.0.0 : Section software-updates
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Any, Optional
import json, threading, datetime
from fastapi import APIRouter, Body, HTTPException, Path, Response
from openapi_server.shared import r, redis_add_log

router = APIRouter()

_PCAT = "ecu2:update:catalog"
_PSTA = "ecu2:update:status"
_IDF  = "id"
_STP  = 10
_SDL  = 1.5
_EVS  = "UPDATE_STARTED"
_EVC  = "UPDATE_COMPLETED"
_EID  = "2"

def _catalog():
    items = []
    for k in r.keys(f"{_PCAT}:*"):
        raw = r.get(k)
        if raw:
            it = json.loads(raw)
            it["ecu_id"] = _EID
            items.append(it)
    return items

def _get_upd(uid):
    raw = r.get(f"{_PCAT}:{uid}")
    return json.loads(raw) if raw else None

def _get_sta(uid):
    raw = r.get(f"{_PSTA}:{uid}")
    return json.loads(raw) if raw else None

def _set_sta(uid, s):
    r.set(f"{_PSTA}:{uid}", json.dumps(s))

def _simulate(uid, ver):
    import time
    for p in range(_STP, 101, _STP):
        time.sleep(_SDL)
        _set_sta(uid, {"id":uid,"version":ver,"ecu_id":_EID,"status":"installing","progress":p})
    _set_sta(uid, {"id":uid,"version":ver,"ecu_id":_EID,"status":"installed","progress":100})
    redis_add_log(event=_EVC, detail=f"ECU 2 - OTA {uid} ({ver}) installed", level="INFO")

@router.get("/ecu/2/updates", response_model=None, tags=["ecu2-updates"], summary="ECU 2 - Get Updates")
async def get_ecu2_updates():
    return {"entity_id":"2","ecu_id":"2","total":len(_catalog()),"updates":_catalog()}

@router.post("/ecu/2/updates", response_model=None, tags=["ecu2-updates"], summary="ECU 2 - Install Update")
async def install_ecu2_update(body: Optional[Any] = Body(None)):
    data = body if isinstance(body, dict) else {}
    uid = data.get(_IDF, "upd-001")
    upd = _get_upd(uid)
    if not upd: raise HTTPException(404, f"Update '{uid}' not found")
    _set_sta(uid, {"id":uid,"version":upd["version"],"ecu_id":"2","status":"installing","progress":0})
    redis_add_log(event=_EVS, detail=f"ECU 2 - OTA {uid} initiated", level="INFO")
    threading.Thread(target=_simulate, args=(uid, upd["version"]), daemon=True).start()
    return {"id":uid,"version":upd["version"],"ecu_id":"2","status":"installing","progress":0}

@router.get("/ecu/2/updates/{uid}", response_model=None, tags=["ecu2-updates"], summary="ECU 2 - Update Status")
async def get_ecu2_update_status(uid: str = Path(...)):
    s = _get_sta(uid)
    if not s: raise HTTPException(404, f"No update '{uid}' for ECU 2")
    return s
