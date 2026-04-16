# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_logs_config_get200_response import EntityCollectionEntityIdLogsConfigGet200Response
from openapi_server.models.entity_collection_entity_id_logs_config_put_request import EntityCollectionEntityIdLogsConfigPutRequest
from openapi_server.models.entity_collection_entity_id_logs_entries_get200_response import EntityCollectionEntityIdLogsEntriesGet200Response


class BaseLoggingApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseLoggingApi.subclasses = BaseLoggingApi.subclasses + (cls,)
    def clear_engine_ecu_logs(
        self,
    ) -> None:
        """Clear all diagnostic logs from the engine ECU."""
        ...


    def entity_collection_entity_id_logs_config_delete(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> None:
        """This method resets the current configuration to its default."""
        ...


    def entity_collection_entity_id_logs_config_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdLogsConfigGet200Response:
        """This method returns an array of configured SOVD LogConfiguration elements, specifying the different contexts for which a specific log configuration was created with the method Configure SOVD Logging."""
        ...


    def entity_collection_entity_id_logs_config_put(
        self,
        entity_collection: str,
        entity_id: str,
        entity_collection_entity_id_logs_config_put_request: EntityCollectionEntityIdLogsConfigPutRequest,
    ) -> None:
        """This method configures the log aggregation."""
        ...


    def entity_collection_entity_id_logs_entries_get(
        self,
        entity_collection: str,
        entity_id: str,
        severity: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdLogsEntriesGet200Response:
        """This method provides the log information aggregated by that entity."""
        ...


    def get_engine_ecu_logs(
        self,
    ) -> List[object]:
        """Retrieve diagnostic logs from the simulated engine ECU."""
        ...
