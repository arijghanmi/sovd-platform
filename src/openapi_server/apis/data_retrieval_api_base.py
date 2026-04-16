# coding: utf-8

from typing import Optional, Any, ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_data_categories_get200_response import EntityCollectionEntityIdDataCategoriesGet200Response
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response import EntityCollectionEntityIdDataDataIdGet200Response
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response_errors_inner import EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner
from openapi_server.models.entity_collection_entity_id_data_data_id_put_request import EntityCollectionEntityIdDataDataIdPutRequest
from openapi_server.models.entity_collection_entity_id_data_get200_response import EntityCollectionEntityIdDataGet200Response
from openapi_server.models.entity_collection_entity_id_data_groups_get200_response import EntityCollectionEntityIdDataGroupsGet200Response
from openapi_server.models.entity_collection_entity_id_data_lists_data_list_id_get200_response import EntityCollectionEntityIdDataListsDataListIdGet200Response
from openapi_server.models.entity_collection_entity_id_data_lists_post201_response import EntityCollectionEntityIdDataListsPost201Response
from openapi_server.models.entity_collection_entity_id_data_lists_post_request import EntityCollectionEntityIdDataListsPostRequest
from openapi_server.models.get_engine_ecu_speed200_response import GetEngineEcuSpeed200Response


class BaseDataRetrievalApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseDataRetrievalApi.subclasses = BaseDataRetrievalApi.subclasses + (cls,)
    def entity_collection_entity_id_data_categories_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdDataCategoriesGet200Response:
        ...


    def entity_collection_entity_id_data_data_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        data_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdDataDataIdGet200Response:
        ...


    def entity_collection_entity_id_data_data_id_put(
        self,
        entity_collection: str,
        entity_id: str,
        data_id: str,
        entity_collection_entity_id_data_data_id_put_request: EntityCollectionEntityIdDataDataIdPutRequest,
    ) -> None:
        ...


    def entity_collection_entity_id_data_get(
        self,
        entity_collection: str,
        entity_id: str,
        groups: str,
        category: List[str],
        include_schema: bool,
    ) -> EntityCollectionEntityIdDataGet200Response:
        ...


    def entity_collection_entity_id_data_groups_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdDataGroupsGet200Response:
        ...


    def entity_collection_entity_id_data_lists_data_list_id_delete(
        self,
        entity_collection: str,
        entity_id: str,
        data_list_id: str,
    ) -> None:
        ...


    def entity_collection_entity_id_data_lists_data_list_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        data_list_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdDataListsDataListIdGet200Response:
        ...


    def entity_collection_entity_id_data_lists_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdDataGroupsGet200Response:
        ...


    def entity_collection_entity_id_data_lists_post(
        self,
        entity_collection: str,
        entity_id: str,
        entity_collection_entity_id_data_lists_post_request: EntityCollectionEntityIdDataListsPostRequest,
    ) -> EntityCollectionEntityIdDataListsPost201Response:
        ...


    def get_engine_ecu_data(
        self,
    ) -> List[object]:
        """Retrieve all available data items from the simulated engine ECU."""
        ...


    def get_engine_ecu_data_by_id(
        self,
        data_id: str,
    ) -> object:
        """Retrieve a specific data item from the engine ECU."""
        ...


    def get_engine_ecu_speed(
        self,
    ) -> GetEngineEcuSpeed200Response:
        """Retrieve the current simulated vehicle speed from the engine ECU."""
        ...


    def get_engine_ecu_speed_events(
        self,
    ) -> str:
        """Server-Sent Events stream for real-time vehicle speed updates. Implements SOVD ResponseOnEvent mechanism (equivalent to UDS 0x86). Pushes speed values every 500ms."""
        ...


    def update_engine_ecu_data(
        self,
        data_id: str,
        body: Optional[Any] = None,
    ) -> None:
        """Write a value to a specific data item of the engine ECU."""
        ...
