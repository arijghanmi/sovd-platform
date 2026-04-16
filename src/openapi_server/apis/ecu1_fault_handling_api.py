# coding: utf-8
# ============================================================
# ecu1_fault_handling_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu1_config.yaml
# Date: 2026-04-16 14:59:27
# Reference ASAM SOVD V1.0.0 : Section faults
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Any, Optional
import json
from fastapi import APIRouter, Body, HTTPException, Path, Query, Response
from openapi_server.shared import r, redis_add_log, redis_add_log_ecu

router = APIRouter()

_PREFIX    = "ecu1:fault"
_CF        = "faultCode"
_DF        = "dtc_type"
_TYPES     = ['ACTIVE', 'PENDING', 'PERMANENT']
_EV_ADD    = "FAULT_ADDED"
_EV_CLR    = "FAULTS_CLEARED"
_EID       = "1"
_PERM_FLAG = "ecu1:driving_cycle_complete"

def _get_all(scope=None):
    faults = []
    for k in r.keys(f"{_PREFIX}:*"):
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
    raw = r.get(f"{_PREFIX}:{fid}")
    if not raw: return None
    f = json.loads(raw)
    f["ecu_id"] = _EID
    return f

def _add(fault):
    code = fault.get(_CF, "UNKNOWN")
    t = fault.get(_DF, "ACTIVE").upper()
    fault[_DF] = t if t in _TYPES else _TYPES[0]
    fault["ecu_id"] = _EID
    r.set(f"{_PREFIX}:{code}", json.dumps(fault))
    return fault

def _delete_all(scope=None):
    deleted = 0
    cycle_done = _PERM_FLAG and r.get(_PERM_FLAG) == "true"
    for k in r.keys(f"{_PREFIX}:*"):
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
    c = {t.lower(): 0 for t in _TYPES}
    for k in r.keys(f"{_PREFIX}:*"):
        try:
            f = json.loads(r.get(k))
            t = f.get(_DF,"ACTIVE").lower()
            if t in c: c[t] += 1
        except: pass
    return c

def _cycle_status():
    if not _PERM_FLAG: return False
    return r.get(_PERM_FLAG) == "true"

@router.get("/ecu/1/faults", response_model=None, tags=["ecu1-faults"], summary="ECU 1 - Get Faults")
async def get_ecu1_faults(scope: Optional[str] = Query(None)):
    faults = _get_all(scope=scope)
    counts = _count()
    return {
        "entity_id":"1","ecu_id":"1",
        "total_faults":sum(counts.values()),
        "faults":faults,"counts_by_type":counts,
        "permanent_clearable": _cycle_status()
    }

@router.post("/ecu/1/faults", response_model=None, tags=["ecu1-faults"], summary="ECU 1 - Add Fault")
async def add_ecu1_fault(body: Optional[Any] = Body(None)):
    if not body: raise HTTPException(400, "Body required")
    data = body if isinstance(body, dict) else body.dict()
    added = _add(data)
    redis_add_log_ecu(event=_EV_ADD, detail=f"ECU 1 - Fault {data.get(_CF,'?')} injected", level="INFO", ecu_id="1")
    return {"message":"Fault added","fault":added}

@router.delete("/ecu/1/faults", response_model=None, tags=["ecu1-faults"], summary="ECU 1 - Clear Faults")
async def clear_ecu1_faults(scope: Optional[str] = Query(None)):
    deleted = _delete_all(scope=scope)
    cycle_was_done = _cycle_status() if deleted == 0 else False
    redis_add_log_ecu(event=_EV_CLR, detail=f"ECU 1 - Cleared {deleted} faults", level="INFO", ecu_id="1")
    return {
        "message":f"{deleted} fault(s) cleared",
        "ecu_id":"1",
        "permanent_cleared": deleted > 0 and not cycle_was_done
    }

@router.get("/ecu/1/faults/{fid}", response_model=None, tags=["ecu1-faults"], summary="ECU 1 - Get Fault By ID")
async def get_ecu1_fault_by_id(fid: str = Path(...)):
    f = _get_by_id(fid)
    if not f: raise HTTPException(404, f"Fault '{fid}' not found in ECU 1")
    return {"fault":f,"found":True}
