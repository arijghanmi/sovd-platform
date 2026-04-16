# coding: utf-8
# ============================================================
# updates_api.py
# 
# FICHIER AUTO-GÉNÉRÉ par generate_routes.py
# Source : ecu_config.yaml
# Date   : 2026-04-08 16:09:41
#
# NE PAS MODIFIER MANUELLEMENT.
# Pour changer la logique, modifier ecu_config.yaml
# puis relancer : python generate_routes.py
#
# Référence ASAM SOVD V1.0.0 : §software-updates — software-updates.yaml
# ============================================================

from typing import Any, List, Optional
import json, threading, datetime

from fastapi import APIRouter, Body, HTTPException, Path, Query, Response
from openapi_server.shared import r, redis_add_log

router = APIRouter()

_PREFIX_CAT    = "update:catalog"
_PREFIX_STATUS = "update:status"
_ID_FIELD      = "id"
_STEP_PCT      = 10
_STEP_DELAY    = 1.5
_EV_START      = "UPDATE_STARTED"
_EV_COMPLETE   = "UPDATE_COMPLETED"

def _get_catalog():
    return [json.loads(r.get(k)) for k in r.keys(f"{_PREFIX_CAT}:*") if r.get(k)]

def _get_by_id(uid: str):
    raw = r.get(f"{_PREFIX_CAT}:{uid}")
    return json.loads(raw) if raw else None

def _get_status(uid: str):
    raw = r.get(f"{_PREFIX_STATUS}:{uid}")
    return json.loads(raw) if raw else None

def _set_status(uid: str, status: dict):
    r.set(f"{_PREFIX_STATUS}:{uid}", json.dumps(status))

def _simulate(uid: str, version: str):
    import time as _time
    for progress in range(_STEP_PCT, 101, _STEP_PCT):
        _time.sleep(_STEP_DELAY)
        _set_status(uid, {
            "id": uid, "version": version,
            "status": "installing", "progress": progress,
            "started_at": datetime.datetime.utcnow().isoformat() + "Z"
        })
    _set_status(uid, {
        "id": uid, "version": version,
        "status": "installed", "progress": 100,
        "completed_at": datetime.datetime.utcnow().isoformat() + "Z"
    })
    redis_add_log(event=_EV_COMPLETE, detail=f"OTA {uid} ({version}) installed", level="INFO")

@router.get("/ecu/engine/updates", response_model=None, tags=["updates"], summary="Get Available Updates")
async def get_engine_ecu_updates():
    updates = _get_catalog()
    return {"entity_id": "engine", "total": len(updates), "updates": updates}

@router.post("/ecu/engine/updates", response_model=None, tags=["updates"], summary="Initiate Software Update")
async def initiate_engine_ecu_update(body: Optional[Any] = Body(None)):
    data = body if isinstance(body, dict) else {}
    uid = data.get(_ID_FIELD, "upd-001")
    update = _get_by_id(uid)
    if not update:
        raise HTTPException(status_code=404, detail=f"Update '{uid}' not found")
    _set_status(uid, {
        "id": uid, "version": update["version"],
        "status": "installing", "progress": 0,
        "started_at": datetime.datetime.utcnow().isoformat() + "Z"
    })
    redis_add_log(event=_EV_START, detail=f"OTA {uid} ({update['version']}) initiated", level="INFO")
    threading.Thread(target=_simulate, args=(uid, update["version"]), daemon=True).start()
    return {"id": uid, "version": update["version"], "status": "installing", "progress": 0}

@router.get("/ecu/engine/updates/{update_id}", response_model=None, tags=["updates"], summary="Get Update Status")
async def get_engine_ecu_update_status(update_id: str = Path(...)):
    s = _get_status(update_id)
    if not s:
        raise HTTPException(status_code=404, detail=f"No active update for '{update_id}'")
    return s

@router.get("/{entity_collection}/{entity_id}/updates", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    target_version: Optional[str] = Query(None, alias="target-version"),
    origin: Optional[str] = Query(None),
):
    updates = _get_catalog()
    return {"entity_id": entity_id, "total": len(updates), "updates": updates}

@router.get("/{entity_collection}/{entity_id}/updates/{update_package_id}", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_package_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    update_package_id: str = Path(...),
):
    return Response(status_code=501)

@router.get("/{entity_collection}/{entity_id}/updates/{update_package_id}/status", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_package_status_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    update_package_id: str = Path(...),
):
    s = _get_status(update_package_id)
    if not s:
        raise HTTPException(status_code=404, detail=f"No status for '{update_package_id}'")
    return s

@router.put("/{entity_collection}/{entity_id}/updates/{update_package_id}/execute", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_execute(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    update_package_id: str = Path(...),
):
    return Response(status_code=501)

@router.put("/{entity_collection}/{entity_id}/updates/{update_package_id}/prepare", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_prepare(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    update_package_id: str = Path(...),
):
    return Response(status_code=501)

@router.delete("/{entity_collection}/{entity_id}/updates/{update_package_id}", response_model=None, tags=["updates"])
async def entity_collection_entity_id_updates_delete(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    update_package_id: str = Path(...),
):
    return Response(status_code=501)
