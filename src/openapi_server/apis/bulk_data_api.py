# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.bulk_data_api_base import BaseBulkDataApi
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
from openapi_server.models.entity_collection_entity_id_bulk_data_get200_response import EntityCollectionEntityIdBulkDataGet200Response


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.get(
    "/{entity-collection}/{entity-id}/bulk-data",
    responses={
        200: {"model": EntityCollectionEntityIdBulkDataGet200Response, "description": "The bulk data categories supported by the entity."},
        200: {"model": AnyPathDocsGetDefaultResponse, "description": "An unexpected error occurred."},
    },
    tags=["bulk-data"],
    response_model_by_alias=True,
)
async def entity_collection_entity_id_bulk_data_get(
    entity_collection: str = Path(..., description="Path to an entity collection"),
    entity_id: str = Path(..., description="ID of an entity"),
    include_schema: bool = Query(None, description="Specifies whether the response should include schema information or not. Default: false", alias="include-schema"),
) -> EntityCollectionEntityIdBulkDataGet200Response:
    """This method provides the list of bulk data categories supported by an entity. The result contains all available and based on the authorization accesible bulk data categories. Certain bulk data categories are hidden based on the user’s authorization."""
    return BaseBulkDataApi.subclasses[0]().entity_collection_entity_id_bulk_data_get(entity_collection, entity_id, include_schema)
