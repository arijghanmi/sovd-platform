# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.locking_api_base import BaseLockingApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_locks_get200_response import EntityCollectionEntityIdLocksGet200Response
from openapi_server.models.entity_collection_entity_id_locks_lock_id_get200_response import EntityCollectionEntityIdLocksLockIdGet200Response
from openapi_server.models.entity_collection_entity_id_locks_post201_response import EntityCollectionEntityIdLocksPost201Response
from openapi_server.models.entity_collection_entity_id_locks_post_request import EntityCollectionEntityIdLocksPostRequest


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/{entity-collection}/{entity-id}/locks",
    responses={
        200: {"model": EntityCollectionEntityIdLocksGet200Response, "description": "The request was successful."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["locking"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_locks_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
) -> EntityCollectionEntityIdLocksGet200Response:
    """The method returns the acquired locks for the given entity."""
    return BaseLockingApi.subclasses[0]().entity_collection_entity_id_locks_get(entity_collection, entity_id)


@router.delete(
    "/{entity-collection}/{entity-id}/locks/{lock-id}",
    responses={
        204: {"description": "The request was successful."},
        409: {"model": AnyPathDocsGetDefaultResponse, "description": "The SOVD server rejected the extension of the lock resource."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["locking"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_locks_lock_id_delete(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    lock_id: str = Path(..., description="The resource identifier of the lock resource to be deleted."),
) -> None:
    """This method releases an acquired lock by deleting the created lock resource."""
    return BaseLockingApi.subclasses[0]().entity_collection_entity_id_locks_lock_id_delete(entity_collection, entity_id, lock_id)


@router.get(
    "/{entity-collection}/{entity-id}/locks/{lock-id}",
    responses={
        200: {"model": EntityCollectionEntityIdLocksLockIdGet200Response, "description": "The request was successful."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["locking"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_locks_lock_id_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    lock_id: str = Path(..., description="The resource identifier of the lock resource to be requested."),
) -> EntityCollectionEntityIdLocksLockIdGet200Response:
    """The method returns all the details on the specified lock of the given entity. For extending the expiration of a lock the method described in 6.11.5 has to be invoked."""
    return BaseLockingApi.subclasses[0]().entity_collection_entity_id_locks_lock_id_get(entity_collection, entity_id, lock_id)


@router.put(
    "/{entity-collection}/{entity-id}/locks/{lock-id}",
    responses={
        204: {"description": "The request was successful."},
        409: {"model": AnyPathDocsGetDefaultResponse, "description": "The SOVD server rejected the extension of the lock resource."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["locking"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_locks_lock_id_put(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    lock_id: str = Path(..., description="Identifier of a previous lock owned by the SOVD client."),
    entity_collection_entity_id_locks_post_request: EntityCollectionEntityIdLocksPostRequest = Body(None, description="Request body - Acquire a lock on an entity"),
) -> None:
    """This method extends an acquired lock by providing a new expiration time. The extension is only valid for the SOVD client that has already acquired the corresponding lock."""
    return BaseLockingApi.subclasses[0]().entity_collection_entity_id_locks_lock_id_put(entity_collection, entity_id, lock_id, entity_collection_entity_id_locks_post_request)


@router.post(
    "/{entity-collection}/{entity-id}/locks",
    responses={
        201: {"model": EntityCollectionEntityIdLocksPost201Response, "description": "The SOVD server has successfully created a new lock resource and acquired a lock on all relevant resources."},
        409: {"model": AnyPathDocsGetDefaultResponse, "description": "The SOVD server rejected the creation of the lock resource."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["locking"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_locks_post(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    entity_collection_entity_id_locks_post_request: EntityCollectionEntityIdLocksPostRequest = Body(None, description="Request body - Acquire a lock on an entity"),
) -> EntityCollectionEntityIdLocksPost201Response:
    """This method acquires a lock from the SOVD server for the given entity to reserve its resources for exclusive access of a single SOVD client, i.e., prevent other SOVD clients from operating on the resources in parallel. Any further requests against the SOVD API towards controlling an operation (actuators, routines, and input control), e.g., start the execution of an operation, is rejected by the SOVD server if the required lock is not acquired by the same SOVD client. Once the lock is not required anymore, the SOVD client can delete the created lock resource by a corresponding DELETE request. In addition, an SOVD client shall provide a relative expiration time after which the SOVD server should release the lock automatically. The SOVD server might reject the requested expiration time if it is too long. As a result, the SOVD server deletes the corresponding lock resource."""
    return BaseLockingApi.subclasses[0]().entity_collection_entity_id_locks_post(entity_collection, entity_id, entity_collection_entity_id_locks_post_request)
