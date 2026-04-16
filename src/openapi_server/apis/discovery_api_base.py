# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.areas_area_id_related_components_get200_response import AreasAreaIdRelatedComponentsGet200Response
from openapi_server.models.entity_collection_entity_id_get200_response import EntityCollectionEntityIdGet200Response
from openapi_server.models.entity_collection_get200_response import EntityCollectionGet200Response


class BaseDiscoveryApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDiscoveryApi.subclasses = BaseDiscoveryApi.subclasses + (cls,)
    def areas_area_id_related_components_get(
        self,
        area_id: str,
    ) -> AreasAreaIdRelatedComponentsGet200Response:
        """This method provides the list of related Components of an Area"""
        ...


    def areas_area_id_subareas_get(
        self,
        area_id: str,
        include_schema: bool,
    ) -> EntityCollectionGet200Response:
        """This method provides the list of sub-entities for each Area."""
        ...


    def components_component_id_related_apps_get(
        self,
        component_id: str,
    ) -> AreasAreaIdRelatedComponentsGet200Response:
        """This method provides the list of related app present on a component"""
        ...


    def components_component_id_subcomponents_get(
        self,
        component_id: str,
        include_schema: bool,
    ) -> EntityCollectionGet200Response:
        """This method provides the list of sub-entities for each Component."""
        ...


    def entity_collection_entity_id_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdGet200Response:
        """This method returns the capabilities of an entity."""
        ...


    def entity_collection_get(
        self,
        entity_collection: str,
        include_schema: bool,
    ) -> EntityCollectionGet200Response:
        """This method provides the list of contained entities for each requested entity collection"""
        ...
