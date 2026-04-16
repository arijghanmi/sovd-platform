# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_configurations_configuration_id_put_request import EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest
from openapi_server.models.entity_collection_entity_id_configurations_get200_response import EntityCollectionEntityIdConfigurationsGet200Response
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response_errors_inner import EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner
from openapi_server.models.entity_collection_entity_id_data_lists_data_list_id_get200_response_items_inner import EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner


class BaseConfigurationsApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseConfigurationsApi.subclasses = BaseConfigurationsApi.subclasses + (cls,)
    def entity_collection_entity_id_configurations_configuration_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        configuration_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner:
        """This method is used to read a configuration from an entity, which can either be * bulk data or * parameter data (MIME type: application/json) The SOVD standard follows the server-driven content negotiation where the client defines its preferences using the Accept request header. If no Accept request header is provided, the SOVD server returns a default representation."""
        ...


    def entity_collection_entity_id_configurations_configuration_id_put(
        self,
        entity_collection: str,
        entity_id: str,
        configuration_id: str,
        entity_collection_entity_id_configurations_configuration_id_put_request: EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest,
    ) -> None:
        """This method is used to write a configuration to an entity, which can either be • bulk data, or • parameter data (MIME type: application/json) The SOVD client shall tell the SOVD server in the Content-Type header, which MIME type is written to it."""
        ...


    def entity_collection_entity_id_configurations_get(
        self,
        entity_collection: str,
        entity_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdConfigurationsGet200Response:
        """Provides the configurations provided by an entity."""
        ...
