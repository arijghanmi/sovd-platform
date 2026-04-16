# coding: utf-8
# ============================================================
# ecu1_logging_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu1_config.yaml
# Date: 2026-04-16 14:59:27
# Reference ASAM SOVD V1.0.0 : Section logs
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Optional
import json
from fastapi import APIRouter, Query, Response
from openapi_server.shared import r

router = APIRouter()

_RKEY = "ecu1:logs:entries"
_LF   = "level"
_MAX  = 200
_EID  = "1"

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

@router.get("/ecu/1/logs", response_model=None, tags=["ecu1-logs"], summary="ECU 1 - Get Logs")
async def get_ecu1_logs(limit: Optional[int] = Query(200), level: Optional[str] = Query(None)):
    logs = _get_logs(limit=limit or _MAX, level=level)
    return {"entity_id":"1","ecu_id":"1","total":len(logs),"entries":logs}

@router.delete("/ecu/1/logs", response_model=None, tags=["ecu1-logs"], summary="ECU 1 - Clear Logs")
async def clear_ecu1_logs():
    r.delete(_RKEY)
    return {"status":"cleared","ecu_id":"1"}
