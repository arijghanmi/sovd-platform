# coding: utf-8
# ============================================================
# logging_api.py
# 
# FICHIER AUTO-GÉNÉRÉ par generate_routes.py
# Source : ecu_config.yaml
# Date   : 2026-04-08 16:09:41
#
# NE PAS MODIFIER MANUELLEMENT.
# Pour changer la logique, modifier ecu_config.yaml
# puis relancer : python generate_routes.py
#
# Référence ASAM SOVD V1.0.0 : §logs — logs.yaml
# ============================================================

from typing import List, Optional
import json

from fastapi import APIRouter, HTTPException, Path, Query, Response
from openapi_server.shared import r

router = APIRouter()

_REDIS_KEY   = "logs:entries"
_LEVEL_FIELD = "level"
_MAX_ENTRIES = 200

def _get_logs(limit: int = 100, level: str = None):
    raw = r.lrange(_REDIS_KEY, -limit, -1)
    entries = []
    for item in raw:
        try:
            entries.append(json.loads(item))
        except Exception:
            pass
    if level:
        entries = [e for e in entries if e.get(_LEVEL_FIELD, "").upper() == level.upper()]
    return list(reversed(entries))

def _clear_logs():
    r.delete(_REDIS_KEY)

@router.get("/ecu/engine/logs", response_model=None, tags=["logging"], summary="Get Engine Diagnostic Logs")
async def get_engine_ecu_logs(
    limit: Optional[int] = Query(200, description="Max entries"),
    level: Optional[str] = Query(None, description="Filter by log level"),
):
    logs = _get_logs(limit=limit or _MAX_ENTRIES, level=level)
    return {"entity_id": "engine", "total": len(logs), "entries": logs}

@router.delete("/ecu/engine/logs", response_model=None, tags=["logging"], summary="Clear Engine Diagnostic Logs")
async def clear_engine_ecu_logs():
    _clear_logs()
    return {"status": "cleared", "entity_id": "engine"}

@router.get("/{entity_collection}/{entity_id}/logs/entries", response_model=None, tags=["logging"])
async def entity_collection_entity_id_logs_entries_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
    severity: Optional[str] = Query(None),
    include_schema: Optional[bool] = Query(None, alias="include-schema"),
):
    logs = _get_logs(limit=_MAX_ENTRIES, level=severity)
    return {"entity_id": entity_id, "total": len(logs), "entries": logs}

@router.get("/{entity_collection}/{entity_id}/logs/config", response_model=None, tags=["logging"])
async def entity_collection_entity_id_logs_config_get(
    entity_collection: str = Path(...), entity_id: str = Path(...),
):
    return Response(status_code=501)

@router.put("/{entity_collection}/{entity_id}/logs/config", response_model=None, tags=["logging"])
async def entity_collection_entity_id_logs_config_put(
    entity_collection: str = Path(...), entity_id: str = Path(...),
):
    return Response(status_code=501)

@router.delete("/{entity_collection}/{entity_id}/logs/config", response_model=None, tags=["logging"])
async def entity_collection_entity_id_logs_config_delete(
    entity_collection: str = Path(...), entity_id: str = Path(...),
):
    return Response(status_code=501)
