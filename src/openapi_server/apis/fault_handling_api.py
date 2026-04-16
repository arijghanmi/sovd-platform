# coding: utf-8
# ============================================================
# fault_handling_api.py
# 
# FICHIER AUTO-GÉNÉRÉ par generate_routes.py
# Source : ecu_config.yaml
# Date   : 2026-04-08 16:09:41
#
# NE PAS MODIFIER MANUELLEMENT.
# Pour changer la logique, modifier ecu_config.yaml
# puis relancer : python generate_routes.py
#
# Référence ASAM SOVD V1.0.0 : §faults — faults.yaml
# ============================================================

from typing import Any, List, Optional
import json

from fastapi import APIRouter, Body, HTTPException, Path, Query, Response
from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.get_fault_by_id200_response import GetFaultById200Response
from openapi_server.models.get_faults200_response import GetFaults200Response
from openapi_server.shared import r, redis_add_log

router = APIRouter()

# --------------------------------------------------------
# Paramètres lus depuis ecu_config.yaml
# --------------------------------------------------------
_PREFIX      = "fault"
_CODE_FIELD  = "faultCode"
_DTC_FIELD   = "dtc_type"
_TYPES       = ['ACTIVE', 'PENDING', 'PERMANENT']
_SCOPE_FIELD = "dtc_type"
_EV_ADD      = "FAULT_ADDED"
_EV_CLEAR    = "FAULTS_CLEARED"
_NO_DELETE   = "PERMANENT"

# --------------------------------------------------------
# Fonctions génériques pilotées par la config
# --------------------------------------------------------

def _get_all(scope=None):
    keys = r.keys(f"{_PREFIX}:*")
    faults = []
    for k in keys:
        try:
            raw = r.get(k)
            if raw:
                faults.append(json.loads(raw))
        except Exception:
            pass
    if scope:
        s = scope.upper()
        if s in _TYPES:
            faults = [f for f in faults if f.get(_DTC_FIELD, "").upper() == s]
        else:
            return []
    return faults

def _get_by_id(fault_id: str):
    raw = r.get(f"{_PREFIX}:{fault_id}")
    return json.loads(raw) if raw else None

def _add(fault: dict):
    code = fault.get(_CODE_FIELD, "UNKNOWN")
    t = fault.get(_DTC_FIELD, "ACTIVE").upper()
    fault[_DTC_FIELD] = t if t in _TYPES else _TYPES[0]
    r.set(f"{_PREFIX}:{code}", json.dumps(fault))
    return fault

def _delete_all(scope=None):
    keys = r.keys(f"{_PREFIX}:*")
    deleted = 0
    for k in keys:
        try:
            f = json.loads(r.get(k))
            t = f.get(_DTC_FIELD, "ACTIVE").upper()
            if scope is None and t != _NO_DELETE:
                r.delete(k); deleted += 1
            elif scope and scope.upper() == t:
                r.delete(k); deleted += 1
        except Exception:
            pass
    return deleted

def _count():
    counts = {t.lower(): 0 for t in _TYPES}
    for k in r.keys(f"{_PREFIX}:*"):
        try:
            f = json.loads(r.get(k))
            t = f.get(_DTC_FIELD, "ACTIVE").upper().lower()
            if t in counts:
                counts[t] += 1
        except Exception:
            pass
    return counts

# --------------------------------------------------------
# Routes concrètes ECU : /ecu/engine/faults
# --------------------------------------------------------

@router.get("/ecu/engine/faults", response_model=None, tags=["fault-handling"],
    summary="Get Engine Faults")
async def get_engine_ecu_faults(
    scope: Optional[str] = Query(None, description="Filter: active, pending, permanent")
):
    faults = _get_all(scope=scope)
    counts = _count()
    return {
        "entity_id": "engine",
        "total_faults": sum(counts.values()),
        "faults": faults,
        "counts_by_type": counts,
    }

@router.post("/ecu/engine/faults", response_model=None, tags=["fault-handling"],
    summary="Add Engine Fault")
async def add_engine_ecu_fault(body: Optional[Any] = Body(None)):
    if not body:
        raise HTTPException(status_code=400, detail="Request body is required")
    data = body if isinstance(body, dict) else body.dict()
    added = _add(data)
    redis_add_log(event=_EV_ADD, detail=f"Fault {data.get(_CODE_FIELD, '?')} injected", level="INFO")
    return {"message": "Fault added", "fault": added}

@router.delete("/ecu/engine/faults", response_model=None, tags=["fault-handling"],
    summary="Clear Engine Faults")
async def clear_engine_ecu_faults(
    scope: Optional[str] = Query(None)
):
    deleted = _delete_all(scope=scope)
    redis_add_log(event=_EV_CLEAR, detail=f"Cleared {deleted} faults on engine ECU", level="INFO")
    return {"message": f"{deleted} fault(s) cleared"}

@router.get("/ecu/engine/faults/{fault_id}", response_model=None, tags=["fault-handling"],
    summary="Get Engine Fault By ID")
async def get_engine_ecu_fault_by_id(fault_id: str = Path(...)):
    fault = _get_by_id(fault_id)
    if not fault:
        raise HTTPException(status_code=404, detail=f"Fault '{fault_id}' not found")
    return {"fault": fault, "found": True}

# --------------------------------------------------------
# Routes génériques SOVD
# --------------------------------------------------------

@router.get("/{entity_collection}/{entity_id}/faults", response_model=None, tags=["fault-handling"])
async def get_faults(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    scope: Optional[str] = Query(None),
    include_schema: Optional[bool] = Query(None, alias="include-schema"),
    severity: Optional[int] = Query(None),
):
    faults = _get_all(scope=scope)
    counts = _count()
    return {"entity_id": entity_id, "total_faults": sum(counts.values()), "faults": faults, "counts_by_type": counts}

@router.delete("/{entity_collection}/{entity_id}/faults", response_model=None, tags=["fault-handling"])
async def delete_all_faults(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    scope: Optional[str] = Query(None),
):
    deleted = _delete_all(scope=scope)
    redis_add_log(event=_EV_CLEAR, detail=f"Cleared {deleted} faults on '{entity_id}'", level="INFO")
    return {"message": f"{deleted} fault(s) cleared for {entity_id}"}

@router.get("/{entity_collection}/{entity_id}/faults/{fault_code}", response_model=None, tags=["fault-handling"])
async def get_fault_by_id(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    fault_code: str = Path(...),
    include_schema: Optional[bool] = Query(None, alias="include-schema"),
):
    fault = _get_by_id(fault_code)
    if not fault:
        raise HTTPException(status_code=404, detail=f"Fault '{fault_code}' not found")
    return {"fault": fault, "found": True}

@router.delete("/{entity_collection}/{entity_id}/faults/{fault_code}", response_model=None, tags=["fault-handling"])
async def delete_fault_by_id(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    fault_code: str = Path(...),
):
    return Response(status_code=501)
