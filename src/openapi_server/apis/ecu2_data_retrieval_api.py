# coding: utf-8
# ============================================================
# ecu2_data_retrieval_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu2_config.yaml
# Date: 2026-04-15 15:26:21
# Reference ASAM SOVD V1.0.0 : Section data
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Any, List, Optional
import asyncio, json, random, datetime
from fastapi import APIRouter, Body, HTTPException, Path, Query, Request, Response
from fastapi.responses import StreamingResponse
from openapi_server.shared import r

router = APIRouter()

_PREFIX = "ecu2:data"
_SDID   = "gear"
_SEV    = "GEAR_UPDATE"
_SINT   = 500 / 1000.0
_SMN    = 1
_SMX    = 8
_SUNIT  = "gear"
_EID    = "2"

def _get_all():
    items = []
    for k in r.keys(f"{_PREFIX}:*"):
        raw = r.get(k)
        if raw:
            it = json.loads(raw)
            it["ecu_id"] = _EID
            items.append(it)
    return items

def _get_by_id(did):
    raw = r.get(f"{_PREFIX}:{did}")
    if not raw: return None
    it = json.loads(raw)
    it["ecu_id"] = _EID
    return it

def _update(did, val):
    key = f"{_PREFIX}:{did}"
    raw = r.get(key)
    if not raw: return None
    it = json.loads(raw)
    it["value"] = val
    it["timestamp"] = datetime.datetime.utcnow().isoformat()+"Z"
    r.set(key, json.dumps(it))
    return it

@router.get("/ecu/2/data", response_model=None, tags=["ecu2-data"], summary="ECU 2 - Get All Data")
async def get_ecu2_data():
    return _get_all()

@router.get("/ecu/2/data/gear/events", response_model=None, tags=["ecu2-data"], summary="ECU 2 - SSE GEAR_UPDATE")
async def get_ecu2_sse(request: Request):
    async def stream():
        try:
            yield 'event: connected\ndata: {"ecu_id":"2","status":"subscribed"}\n\n'
            while True:
                if await request.is_disconnected(): break
                try:
                    raw = r.get(f"{_PREFIX}:{_SDID}")
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
                payload = json.dumps({"event":_SEV,"ecu_id":"2","data":{"id":_SDID,"value":val,"unit":_SUNIT if val != "ff" else "unavailable","timestamp":datetime.datetime.utcnow().isoformat()+"Z"}})
                yield f"event: {_SEV}\ndata: {payload}\n\n"
                await asyncio.sleep(_SINT)
        except asyncio.CancelledError: pass
    return StreamingResponse(stream(), media_type="text/event-stream",
        headers={"Cache-Control":"no-cache","X-Accel-Buffering":"no","Connection":"keep-alive"})

@router.get("/ecu/2/data/gear", response_model=None, tags=["ecu2-data"], summary="ECU 2 - Get gear")
async def get_ecu2_gear():
    try:
        raw = r.get(f"{_PREFIX}:{_SDID}")
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
    return {"data_id":_SDID,"ecu_id":"2","value":val,"unit":_SUNIT if val != "ff" else "unavailable","status":status,"timestamp":datetime.datetime.utcnow().isoformat()+"Z"}

@router.get("/ecu/2/data/{data_id}", response_model=None, tags=["ecu2-data"], summary="ECU 2 - Get Data By ID")
async def get_ecu2_data_by_id(data_id: str = Path(...)):
    it = _get_by_id(data_id)
    if not it: raise HTTPException(404, f"Data '{data_id}' not found in ECU 2")
    return it

@router.put("/ecu/2/data/{data_id}", response_model=None, tags=["ecu2-data"], summary="ECU 2 - Update Data")
async def update_ecu2_data(data_id: str = Path(...), body: Optional[Any] = Body(None)):
    val = body.get("value") if isinstance(body, dict) else body
    res = _update(data_id, val)
    if not res: raise HTTPException(404, f"Data '{data_id}' not found in ECU 2")
    return {"status":"updated","data_id":data_id,"ecu_id":"2"}
