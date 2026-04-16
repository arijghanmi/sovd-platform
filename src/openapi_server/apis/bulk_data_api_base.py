# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_bulk_data_get200_response import EntityCollectionEntityIdBulkDataGet200Response


class BaseBulkDataApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseBulkDataApi.subclasses = BaseBulkDataApi.subclasses + (cls,)
    def entity_collection_entity_id_bulk_data_get(
        self,
        entity_collection: str,
        entity_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdBulkDataGet200Response:
        """This method provides the list of bulk data categories supported by an entity. The result contains all available and based on the authorization accesible bulk data categories. Certain bulk data categories are hidden based on the user’s authorization."""
        ...
