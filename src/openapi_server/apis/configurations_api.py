# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.configurations_api_base import BaseConfigurationsApi
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
from openapi_server.models.entity_collection_entity_id_configurations_configuration_id_put_request import EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest
from openapi_server.models.entity_collection_entity_id_configurations_get200_response import EntityCollectionEntityIdConfigurationsGet200Response
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response_errors_inner import EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner
from openapi_server.models.entity_collection_entity_id_data_lists_data_list_id_get200_response_items_inner import EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/{entity-collection}/{entity-id}/configurations/{configuration-id}",
    responses={
        200: {"model": EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner, "description": "Response: Read Configurations"},
        406: {"description": "bulk data: The configuration cannot be provided in the requested MIME type. parameter data: The configuration cannot be provided as parameter data, i.e., the configuration cannot be provided as JSON."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["configurations"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_configurations_configuration_id_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    configuration_id: str = Path(..., description="The identifier for the configuration"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner:
    """This method is used to read a configuration from an entity, which can either be * bulk data or * parameter data (MIME type: application/json) The SOVD standard follows the server-driven content negotiation where the client defines its preferences using the Accept request header. If no Accept request header is provided, the SOVD server returns a default representation."""
    return BaseConfigurationsApi.subclasses[0]().entity_collection_entity_id_configurations_configuration_id_get(entity_collection, entity_id, configuration_id, include_schema)


@router.put(
    "/{entity-collection}/{entity-id}/configurations/{configuration-id}",
    responses={
        204: {"description": "Configuration written."},
        400: {"model": EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner, "description": "The request body does either not contain all required parameter values or the signature for the provided values is wrong. (only applicable for writing parameter data)"},
        409: {"model": AnyPathDocsGetDefaultResponse, "description": "Unable to write configuration due to unsatisfied precondition. E.g., after satisfying precondition “vehicle not in motion” this should be possible."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["configurations"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_configurations_configuration_id_put(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    configuration_id: str = Path(..., description="The identifier for the configuration"),
    entity_collection_entity_id_configurations_configuration_id_put_request: EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest = Body(None, description="Request: Write a data value data to an entity"),
) -> None:
    """This method is used to write a configuration to an entity, which can either be • bulk data, or • parameter data (MIME type: application/json) The SOVD client shall tell the SOVD server in the Content-Type header, which MIME type is written to it."""
    return BaseConfigurationsApi.subclasses[0]().entity_collection_entity_id_configurations_configuration_id_put(entity_collection, entity_id, configuration_id, entity_collection_entity_id_configurations_configuration_id_put_request)


@router.get(
    "/{entity-collection}/{entity-id}/configurations",
    responses={
        200: {"model": EntityCollectionEntityIdConfigurationsGet200Response, "description": "The request was successful"},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["configurations"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_configurations_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdConfigurationsGet200Response:
    """Provides the configurations provided by an entity."""
    return BaseConfigurationsApi.subclasses[0]().entity_collection_entity_id_configurations_get(entity_collection, entity_id, include_schema)
