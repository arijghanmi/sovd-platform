# coding: utf-8

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse, HTMLResponse
import os

# ── Anciens routers (ECU engine — compatibilité) ──────────────
from openapi_server.apis.fault_handling_api import router as fault_router
from openapi_server.apis.data_retrieval_api import router as data_router
from openapi_server.apis.logging_api import router as logging_router
from openapi_server.apis.updates_api import router as updates_router
from openapi_server.apis.locking_api import router as locking_router
from openapi_server.apis.bulk_data_api import router as bulkdata_router
from openapi_server.apis.capabilities_api import router as capabilities_router
from openapi_server.apis.configurations_api import router as configurations_router
from openapi_server.apis.target_modes_api import router as modes_router
from openapi_server.apis.operations_control_api import router as operations_router

# ── ECU 1 — Engine ────────────────────────────────────────────
from openapi_server.apis.ecu1_fault_handling_api import router as ecu1_fault_router
from openapi_server.apis.ecu1_data_retrieval_api import router as ecu1_data_router
from openapi_server.apis.ecu1_logging_api import router as ecu1_log_router
from openapi_server.apis.ecu1_updates_api import router as ecu1_upd_router
from openapi_server.apis.ecu1_capabilities_api import router as ecu1_cap_router

# ── ECU 2 — Transmission ──────────────────────────────────────
from openapi_server.apis.ecu2_fault_handling_api import router as ecu2_fault_router
from openapi_server.apis.ecu2_data_retrieval_api import router as ecu2_data_router
from openapi_server.apis.ecu2_logging_api import router as ecu2_log_router
from openapi_server.apis.ecu2_updates_api import router as ecu2_upd_router
from openapi_server.apis.ecu2_capabilities_api import router as ecu2_cap_router

# ── Discovery commun (retourne ECU 1 + ECU 2) ─────────────────
from openapi_server.apis.discovery_api import router as discovery_router

from openapi_server.shared import redis_count, r
from openapi_server.apis.redis_init_multi import redis_init_all_ecus

app = FastAPI(
    title="SOVD API - FastAPI — Multi-ECU",
    description="Service-Oriented Vehicle Diagnostics API — ECU 1 (Engine) + ECU 2 (Transmission)",
    version="1.0.0",
    docs_url="/swagger-ui/index.html",
    redoc_url="/redoc",
    openapi_url="/v3/api-docs"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# ROUTES PRIORITAIRES
# ============================================================

@app.get("/dashboard", response_class=HTMLResponse, include_in_schema=False)
async def dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "dashboard_sovd.html")
    if os.path.exists(dashboard_path):
        with open(dashboard_path, "r") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>Dashboard not found</h1>", status_code=404)

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/dashboard")

@app.get("/components", summary="Health Check", tags=["Health"])
async def components():
    counts = redis_count()
    return {
        "status": "UP",
        "application": "SOVD API FastAPI — Multi-ECU",
        "version": "1.0.0",
        "ecus": ["ECU 1 — Engine", "ECU 2 — Transmission"],
        "framework": "FastAPI",
        "storage": "Redis",
        "active_faults_count": counts["active"],
        "pending_faults_count": counts["pending"],
        "permanent_faults_count": counts["permanent"],
    }

@app.get("/health", summary="Health Status", tags=["Health"])
async def health():
    import time
    try:
        r.ping()
        redis_status = "connected"
    except Exception:
        redis_status = "disconnected"
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "redis": redis_status
    }
@app.get("/ecu/{eid}/config", response_model=None, tags=["capabilities"])
async def ecu_config(eid: str):
    import yaml, os
    path = os.path.join(os.path.dirname(__file__), f"ecu{eid}_config.yaml")
    if not os.path.exists(path):
        from fastapi import HTTPException
        raise HTTPException(404, f"Config not found for ECU {eid}")
    with open(path) as f:
        return yaml.safe_load(f)
# ============================================================
# ENREGISTREMENT DES ROUTERS
# ============================================================

# ECU 1 — Engine (/ecu/1/...)
app.include_router(ecu1_fault_router)
app.include_router(ecu1_data_router)
app.include_router(ecu1_log_router)
app.include_router(ecu1_upd_router)
app.include_router(ecu1_cap_router)

# ECU 2 — Transmission (/ecu/2/...)
app.include_router(ecu2_fault_router)
app.include_router(ecu2_data_router)
app.include_router(ecu2_log_router)
app.include_router(ecu2_upd_router)
app.include_router(ecu2_cap_router)

# Anciens routers (/ecu/engine/...) — compatibilité
app.include_router(fault_router)
app.include_router(data_router)
app.include_router(logging_router)
app.include_router(updates_router)
app.include_router(locking_router)
app.include_router(bulkdata_router)
app.include_router(capabilities_router)
app.include_router(configurations_router)
app.include_router(modes_router)
app.include_router(operations_router)

# Discovery EN DERNIER
app.include_router(discovery_router)

# ============================================================
# STARTUP / SHUTDOWN
# ============================================================
@app.on_event("startup")
async def startup_event():
    redis_init_all_ecus()
    print("=" * 60)
    print("  SOVD API FastAPI — Multi-ECU")
    print("  Dashboard  : http://0.0.0.0:8081/dashboard")
    print("  Swagger    : http://0.0.0.0:8081/swagger-ui/index.html")
    print("  ECU 1      : http://0.0.0.0:8081/ecu/1/faults")
    print("  ECU 2      : http://0.0.0.0:8081/ecu/2/faults")
    print("  Discovery  : http://0.0.0.0:8081/ecu")
    try:
        r.ping()
        ecu1_keys = len(r.keys("ecu1:*"))
        ecu2_keys = len(r.keys("ecu2:*"))
        print(f"  Redis      : CONNECTED")
        print(f"  ECU1 keys  : {ecu1_keys}")
        print(f"  ECU2 keys  : {ecu2_keys}")
    except Exception as e:
        print(f"  Redis      : ERREUR - {e}")
    print("=" * 60)

@app.on_event("shutdown")
async def shutdown_event():
    print("SOVD API FastAPI — Shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8081,
                log_level="info", access_log=True)
