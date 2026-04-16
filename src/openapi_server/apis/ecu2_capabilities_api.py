# coding: utf-8
# ============================================================
# ecu2_capabilities_api.py
# AUTO-GENERE par generate_routes.py - Source: ecu2_config.yaml
# Date: 2026-04-16 14:59:27
# Reference ASAM SOVD V1.0.0 : Section capabilities
# NE PAS MODIFIER MANUELLEMENT
# ============================================================

from typing import Optional
import yaml, json
from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

router = APIRouter()

_DESC = "ECU 2 Transmission — SOVD Online Capability Description"
_EID  = "2"
_EC   = "ecu"

def _load_openapi():
    with open("/home/pi/pfe1/sovd-server-fastapi-new/openapi.yaml","r") as f:
        spec = yaml.safe_load(f)
    return json.loads(json.dumps(spec, default=str))

def _ecu_capabilities():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu2_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    ecu = cfg["ecu"]
    disc = ecu["discovery"]
    data_ids = [d["id"] for d in ecu["data"]["initial_data"]]
    resources = [r["name"] for r in disc["resources"]]
    endpoints = [f"GET /ecu/2/{r}".format() for r in resources]
    endpoints += [f"POST /ecu/2/faults",
                  f"DELETE /ecu/2/faults",
                  "PUT /ecu/2/data/{data_id}"]
    return {
        "title":           f"ECU 2 Capability Description",
        "version":         "1.0.0",
        "description":     _DESC,
        "entity":          f"ecu/2",
        "ecu_id":          "2",
        "name":            disc["name"],
        "resources":       resources,
        "data_ids":        data_ids,
        "endpoints":       endpoints,
        "endpoints_count": len(endpoints),
        "sovd_standard":   "ASAM SOVD V1.0.0",
        "mode":            "online",
        "config_source":   f"ecu2_config.yaml"
    }

@router.get("/ecu/2/docs", response_model=None, tags=["ecu2-capabilities"], summary="ECU 2 - Capabilities")
async def get_ecu2_caps(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if include_schema:
        return JSONResponse(_load_openapi())
    return JSONResponse(_ecu_capabilities())

@router.get("/ecu/2/config", response_model=None, tags=["ecu2-capabilities"], summary="ECU 2 - Config YAML")
async def get_ecu2_config():
    import os
    cfg_path = os.path.join(os.path.dirname(__file__), "..", f"ecu2_config.yaml")
    with open(cfg_path, "r") as f:
        cfg = yaml.safe_load(f)
    return JSONResponse(cfg)
