# coding: utf-8
# ============================================================
# ecu1_capabilities_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu1_config.yaml
# Date: 2026-04-15 15:26:21
# Reference ASAM SOVD V1.0.0 : Section capabilities
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Optional
import yaml, json
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

_DESC = "ECU 1 Engine — SOVD Online Capability Description"
_EID  = "1"
_EC   = "ecu"

def _load_openapi():
    with open("/home/pi/pfe1/sovd-server-fastapi-new/openapi.yaml","r") as f:
        spec = yaml.safe_load(f)
    return json.loads(json.dumps(spec, default=str))

def _ecu_capabilities():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu1_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    ecu = cfg["ecu"]
    disc = ecu["discovery"]
    data_ids = [d["id"] for d in ecu["data"]["initial_data"]]
    resources = [r["name"] for r in disc["resources"]]
    endpoints = [f"GET /ecu/1/{r}".format() for r in resources]
    endpoints += [f"POST /ecu/1/faults",
                  f"DELETE /ecu/1/faults",
                  "PUT /ecu/1/data/{data_id}"]
    return {
        "title":           f"ECU 1 Capability Description",
        "version":         "1.0.0",
        "description":     _DESC,
        "entity":          f"ecu/1",
        "ecu_id":          "1",
        "name":            disc["name"],
        "resources":       resources,
        "data_ids":        data_ids,
        "endpoints":       endpoints,
        "endpoints_count": len(endpoints),
        "sovd_standard":   "ASAM SOVD V1.0.0",
        "mode":            "online",
        "config_source":   f"ecu1_config.yaml"
    }

@router.get("/ecu/1/docs", response_model=None, tags=["ecu1-capabilities"], summary="ECU 1 - Capabilities")
async def get_ecu1_caps(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if include_schema:
        return JSONResponse(_load_openapi())
    return JSONResponse(_ecu_capabilities())

@router.get("/ecu/1/config", response_model=None, tags=["ecu1-capabilities"], summary="ECU 1 - Config YAML")
async def get_ecu1_config():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu1_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    return JSONResponse(cfg)
