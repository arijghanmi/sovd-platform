# coding: utf-8
# ============================================================
# capabilities_api.py
# 
# FICHIER AUTO-GÉNÉRÉ par generate_routes.py
# Source : ecu_config.yaml
# Date   : 2026-04-08 16:09:41
#
# NE PAS MODIFIER MANUELLEMENT.
# Pour changer la logique, modifier ecu_config.yaml
# puis relancer : python generate_routes.py
#
# Référence ASAM SOVD V1.0.0 : §capabilities — Online Capability Description
# ============================================================

from typing import Optional
import yaml, os

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

_YAML_FILE   = "openapi.yaml"
_DESCRIPTION = "SOVD Online Capability Description — self-describing ECU"
_EC          = "ecu"
_EID         = "engine"

def _load_spec():
    """Charge openapi.yaml depuis la racine du projet."""
    import json
    path = "/home/pi/pfe1/sovd-server-fastapi-new/openapi.yaml"
    with open(path, "r") as f:
        spec = yaml.safe_load(f)
    return json.loads(json.dumps(spec, default=str))

def _summary(spec: dict, entity: str) -> dict:
    return {
        "title":           spec["info"]["title"],
        "version":         spec["info"]["version"],
        "description":     _DESCRIPTION,
        "entity":          entity,
        "endpoints_count": len(spec.get("paths", {})),
        "sovd_standard":   "ASAM SOVD V1.0.0",
        "mode":            "online"
    }

@router.get("/ecu/engine/docs", response_model=None, tags=["capabilities"],
    summary="SOVD Capability Description — Online Mode")
async def get_engine_ecu_capabilities(
    include_schema: Optional[bool] = Query(False, alias="include-schema")
):
    spec = _load_spec()
    if include_schema:
        return JSONResponse(spec)
    return JSONResponse(_summary(spec, f"{_EC}/{_EID}"))

@router.get("/{entity_collection}/{entity_id}/docs", response_model=None, tags=["capabilities"])
async def entity_collection_entity_id_docs_get(
    entity_collection: str,
    entity_id: str,
    include_schema: Optional[bool] = Query(False, alias="include-schema")
):
    spec = _load_spec()
    if include_schema:
        return JSONResponse(spec)
    return JSONResponse(_summary(spec, f"{entity_collection}/{entity_id}"))
