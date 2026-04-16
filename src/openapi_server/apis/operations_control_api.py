# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.operations_control_api_base import BaseOperationsControlApi
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
from openapi_server.models.entity_collection_entity_id_operations_get200_response import EntityCollectionEntityIdOperationsGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post202_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post_request import EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_get200_response import EntityCollectionEntityIdOperationsOperationIdGet200Response


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/{entity-collection}/{entity-id}/operations",
    responses={
        200: {"model": EntityCollectionEntityIdOperationsGet200Response, "description": "The request was successful"},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    include_proximity_proof: bool = Query(None, description="Specifies whether operations which require a proximity proof are returned or not. The default is true.", alias="include-proximity-proof"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdOperationsGet200Response:
    """This method returns all available operations defined for the given entity."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_get(entity_collection, entity_id, include_proximity_proof, include_schema)


@router.delete(
    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}",
    responses={
        204: {"description": "The request was successful."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_executions_execution_id_delete(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
    execution_id: str = Path(..., description="Identifier for the operation execution"),
    entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request: EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest = Body(None, description="Request: Stop the execution of an operation"),
) -> None:
    """This method terminates the execution of the operation and removes it, and the status of the operation can no longer be requested."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_executions_execution_id_delete(entity_collection, entity_id, operation_id, execution_id, entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request)


@router.get(
    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}",
    responses={
        200: {"model": EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response, "description": "The request was successful."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_executions_execution_id_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
    execution_id: str = Path(..., description="Identifier for the operation execution"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response:
    """This method returns the current status of the operation execution."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_executions_execution_id_get(entity_collection, entity_id, operation_id, execution_id, include_schema)


@router.put(
    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}",
    responses={
        202: {"model": EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response, "description": "The execution of the capability has been triggered by the SOVD server. The successful response code does not indicate that the operation has executed the capability successfully."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_executions_execution_id_put(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
    execution_id: str = Path(..., description="Identifier for the operation execution"),
    entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request: EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest = Body(None, description="Request: Support for execute / freeze / reset and OEM-specific capabilities"),
) -> EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response:
    """This method executes the given capability on the provided operation."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_executions_execution_id_put(entity_collection, entity_id, operation_id, execution_id, entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request)


@router.get(
    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions",
    responses={
        200: {"model": EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response, "description": "The request was successful."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_executions_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
) -> EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response:
    """This method returns currently existing executions of the given operation."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_executions_get(entity_collection, entity_id, operation_id)


@router.post(
    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions",
    responses={
        200: {"model": EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response, "description": "The operation returned immediately, and the response body contains the final result of the operation (“synchronous execution”)."},
        202: {"model": EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response, "description": "The execution of the operation has been triggered by the SOVD server. The successful response code does not indicate that the operation has been started successfully. An SOVD client would then use the method for retrieving the status to request the status of this particular execution instance of the operation (“asynchronous execution”)."},
        409: {"model": AnyPathDocsGetDefaultResponse, "description": "The method is currently not available, e.g., because the operation is still executing."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_executions_post(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
    entity_collection_entity_id_operations_operation_id_executions_post_request: EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest = Body(None, description="Request: Start execution of an operation"),
) -> EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response:
    """Start Execution of an Operation An operation may support multiple executions in parallel. If this is not supported, this method will return an error if an operation with the same operation-id is already being executed. A successfully started operation is added to the executions collection if it is executed asynchronously. After the asynchronous execution has been finished, the execution resource remains existent and an SOVD client can receive the status. However, the status of the execution cannot be queried indefinitely as an SOVD server implementation may remove the resource, e.g., upon SOVD server restart."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_executions_post(entity_collection, entity_id, operation_id, entity_collection_entity_id_operations_operation_id_executions_post_request)


@router.get(
    "/{entity-collection}/{entity-id}/operations/{operation-id}",
    responses={
        200: {"model": EntityCollectionEntityIdOperationsOperationIdGet200Response, "description": "The request was successful"},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["operations-control"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_operations_operation_id_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    operation_id: str = Path(..., description="Identifier for the operation"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdOperationsOperationIdGet200Response:
    """This method returns all the details on the specified operation of the given entity."""
    return BaseOperationsControlApi.subclasses[0]().entity_collection_entity_id_operations_operation_id_get(entity_collection, entity_id, operation_id, include_schema)
