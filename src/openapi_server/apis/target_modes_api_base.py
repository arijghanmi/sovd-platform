# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_modes_get200_response import EntityCollectionEntityIdModesGet200Response


class BaseTargetModesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTargetModesApi.subclasses = BaseTargetModesApi.subclasses + (cls,)
    def entity_collection_entity_id_modes_get(
        self,
        entity_collection: str,
        entity_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdModesGet200Response:
        """This method returns all available modes defined for the given entity."""
        ...
