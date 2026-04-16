# coding: utf-8
# ============================================================
# discovery_api.py - Multi-ECU Discovery
# AUTO-GENERE par generate_routes.py
# Date: 2026-04-15 15:26:21
# Reference ASAM SOVD V1.0.0 : Section 5.1 Discovery
# ============================================================

from typing import Optional
from fastapi import APIRouter, HTTPException, Path, Query, Response
from fastapi.responses import JSONResponse

router = APIRouter()

_EC = "ecu"
_RESERVED = {"dashboard","health","components","swagger-ui","redoc","v3","areas","docs","openapi.json"}

_ALL_ECUS = [
    {"id":"1","name":"Engine ECU","description":"ECU 1 — Simulated Engine ECU — ASAM SOVD V1.0.0","href":"/ecu/1"},
    {"id":"2","name":"Transmission ECU","description":"ECU 2 — Simulated Transmission ECU — ASAM SOVD V1.0.0","href":"/ecu/2"}
]

@router.get("/ecu", response_model=None, tags=["discovery"], summary="List All ECUs")
async def get_all_ecus(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    return JSONResponse({"items": _ALL_ECUS})


@router.get("/ecu/1", response_model=None, tags=["discovery"], summary="ECU 1 Entity")
async def get_entity_1(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    r = {"id":"1","name":"Engine ECU","description":"ECU 1 — Simulated Engine ECU — ASAM SOVD V1.0.0","sovd_standard":"ASAM SOVD V1.0.0"}
    r.update({'faults': '/ecu/1/faults', 'data': '/ecu/1/data', 'logs': '/ecu/1/logs', 'updates': '/ecu/1/updates', 'docs': '/ecu/1/docs'})
    return JSONResponse(r)

@router.get("/ecu/2", response_model=None, tags=["discovery"], summary="ECU 2 Entity")
async def get_entity_2(include_schema: Optional[bool] = Query(False, alias="include-schema")):
    r = {"id":"2","name":"Transmission ECU","description":"ECU 2 — Simulated Transmission ECU — ASAM SOVD V1.0.0","sovd_standard":"ASAM SOVD V1.0.0"}
    r.update({'faults': '/ecu/2/faults', 'data': '/ecu/2/data', 'logs': '/ecu/2/logs', 'updates': '/ecu/2/updates', 'docs': '/ecu/2/docs'})
    return JSONResponse(r)


@router.get("/{entity_collection}/{entity_id}", response_model=None, tags=["discovery"])
async def entity_get(entity_collection: str = Path(...), entity_id: str = Path(...),
    include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if entity_collection in _RESERVED or entity_id in _RESERVED:
        raise HTTPException(404, "Not found")
    for ecu in _ALL_ECUS:
        if entity_collection == _EC and entity_id == ecu["id"]:
            return JSONResponse(ecu)
    return JSONResponse({"id":entity_id,"entity_collection":entity_collection,"status":"multi-ECU environment"})

@router.get("/{entity_collection}", response_model=None, tags=["discovery"])
async def collection_get(entity_collection: str = Path(...),
    include_schema: Optional[bool] = Query(False, alias="include-schema")):
    if entity_collection in _RESERVED:
        raise HTTPException(404, "Not a SOVD entity collection")
    if entity_collection == _EC:
        return JSONResponse({"items": _ALL_ECUS})
    return JSONResponse({"items": []})

@router.get("/areas/{aid}/subareas", response_model=None, tags=["discovery"])
async def areas_sub(aid: str = Path(...)): return Response(status_code=501)

@router.get("/components/{cid}/subcomponents", response_model=None, tags=["discovery"])
async def components_sub(cid: str = Path(...)): return Response(status_code=501)
