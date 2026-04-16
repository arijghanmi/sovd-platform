# coding: utf-8
# ============================================================
# data_retrieval_api.py
# 
# FICHIER AUTO-GÉNÉRÉ par generate_routes.py
# Source : ecu_config.yaml
# Date   : 2026-04-08 16:09:41
#
# NE PAS MODIFIER MANUELLEMENT.
# Pour changer la logique, modifier ecu_config.yaml
# puis relancer : python generate_routes.py
#
# Référence ASAM SOVD V1.0.0 : §data — data.yaml
# ============================================================

from typing import Any, Dict, List, Optional
import asyncio, json, random, datetime

from fastapi import APIRouter, Body, HTTPException, Path, Query, Request, Response
from fastapi.responses import StreamingResponse
from openapi_server.shared import r

router = APIRouter()

_PREFIX   = "data"
_ID_FIELD = "id"
_SSE_DID      = "speed"
_SSE_EVENT    = "SPEED_UPDATE"
_SSE_INTERVAL = 500 / 1000.0
_SSE_MIN      = 20
_SSE_MAX      = 160
_SSE_UNIT     = "km/h"

def _get_all():
    return [json.loads(r.get(k)) for k in r.keys(f"{_PREFIX}:*") if r.get(k)]

def _get_by_id(did: str):
    raw = r.get(f"{_PREFIX}:{did}")
    return json.loads(raw) if raw else None

def _update(did: str, new_value):
    key = f"{_PREFIX}:{did}"
    raw = r.get(key)
    if not raw:
        return None
    item = json.loads(raw)
    item["value"] = new_value
    item["timestamp"] = datetime.datetime.utcnow().isoformat() + "Z"
    r.set(key, json.dumps(item))
    return item

@router.get("/ecu/engine/data", response_model=None, tags=["data-retrieval"], summary="Get All ECU Data")
async def get_engine_ecu_data():
    return _get_all()

@router.get("/ecu/engine/data/speed/events", response_model=None, tags=["data-retrieval"],
    summary="SSE — SPEED_UPDATE ResponseOnEvent")
async def get_engine_ecu_speed_events(request: Request):
    async def stream():
        try:
            yield 'event: connected\ndata: {"status": "subscribed", "endpoint": "/ecu/engine/data/speed/events"}\n\n'
            while True:
                if await request.is_disconnected():
                    break
                try:
                    raw = r.get(f"{_PREFIX}:{_SSE_DID}")
                    if raw:
                        item = json.loads(raw)
                        val = item.get("value", 0)
                        value = round(float(val), 1) if val not in ["ff", "unavailable", None] else 0.0
                    else:
                        value = 0.0
                except Exception:
                    value = round(random.uniform(_SSE_MIN, _SSE_MAX), 1)
                payload = json.dumps({
                    "event": _SSE_EVENT,
                    "data": {"id": _SSE_DID, "value": value, "unit": _SSE_UNIT,
                        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}
                })
                yield f"event: {_SSE_EVENT}\ndata: {payload}\n\n"
                await asyncio.sleep(_SSE_INTERVAL)
        except asyncio.CancelledError:
            pass
    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no", "Connection": "keep-alive"})

@router.get("/ecu/engine/data/speed", response_model=None, tags=["data-retrieval"], summary="Get Vehicle Speed")
async def get_engine_ecu_speed():
    try:
        raw = r.get(f"{_PREFIX}:{_SSE_DID}")
        if raw:
            item = json.loads(raw)
            val = item.get("value", 0)
            value = round(float(val), 1) if val not in ["ff", "unavailable", None] else 0.0
        else:
            value = 0.0
    except Exception:
        value = round(random.uniform(_SSE_MIN, _SSE_MAX), 1)
    return {
        "data_id": _SSE_DID,
        "value": value,
        "unit": _SSE_UNIT,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
    }

@router.get("/ecu/engine/data/{data_id}", response_model=None, tags=["data-retrieval"], summary="Get ECU Data By ID")
async def get_engine_ecu_data_by_id(data_id: str = Path(...)):
    item = _get_by_id(data_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Data '{data_id}' not found")
    return item

@router.put("/ecu/engine/data/{data_id}", response_model=None, tags=["data-retrieval"], summary="Update ECU Data")
async def update_engine_ecu_data(data_id: str = Path(...), body: Optional[Any] = Body(None)):
    value = body.get("value") if isinstance(body, dict) else body
    result = _update(data_id, value)
    if not result:
        raise HTTPException(status_code=404, detail=f"Data '{data_id}' not found")
    return {"status": "updated", "data_id": data_id}

@router.get("/{entity_collection}/{entity_id}/data", response_model=None, tags=["data-retrieval"])
async def entity_collection_entity_id_data_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    groups: Optional[str] = Query(None), category: Optional[List[str]] = Query(None),
    include_schema: Optional[bool] = Query(None, alias="include-schema"),
):
    return _get_all()

@router.get("/{entity_collection}/{entity_id}/data/{data_id}", response_model=None, tags=["data-retrieval"])
async def entity_collection_entity_id_data_data_id_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    data_id: str = Path(...),
    include_schema: Optional[bool] = Query(None, alias="include-schema"),
):
    item = _get_by_id(data_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"Data '{data_id}' not found")
    return item

@router.put("/{entity_collection}/{entity_id}/data/{data_id}", response_model=None, tags=["data-retrieval"])
async def entity_collection_entity_id_data_data_id_put(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    data_id: str = Path(...), body: Optional[Any] = Body(None),
):
    return Response(status_code=501)

@router.get("/{entity_collection}/{entity_id}/data-categories", response_model=None, tags=["data-retrieval"])
async def entity_collection_entity_id_data_categories_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
):
    return {"categories": [{"id": "engine", "name": "Engine Data"}, {"id": "sensors", "name": "Sensor Data"}]}

@router.get("/{entity_collection}/{entity_id}/data-groups", response_model=None, tags=["data-retrieval"])
async def entity_collection_entity_id_data_groups_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
):
    return {"groups": [{"id": "powertrain", "name": "Powertrain"}, {"id": "chassis", "name": "Chassis"}]}
