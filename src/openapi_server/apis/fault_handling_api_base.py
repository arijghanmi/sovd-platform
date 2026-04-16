# coding: utf-8

from typing import Optional, Any, ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.get_fault_by_id200_response import GetFaultById200Response
from openapi_server.models.get_faults200_response import GetFaults200Response


class BaseFaultHandlingApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseFaultHandlingApi.subclasses = BaseFaultHandlingApi.subclasses + (cls,)
    def add_engine_ecu_fault(
        self,
        body: Optional[Any] = None,
    ) -> None:
        """Inject a simulated fault into the engine ECU (for testing purposes)."""
        ...


    def clear_engine_ecu_faults(
        self,
    ) -> None:
        """Delete all faults from the simulated engine ECU."""
        ...


    def delete_all_faults(
        self,
        entity_collection: str,
        entity_id: str,
        scope: str,
    ) -> None:
        """This method deletes all fault entries of an entity."""
        ...


    def delete_fault_by_id(
        self,
        entity_collection: str,
        entity_id: str,
        fault_code: str,
    ) -> None:
        """This method deletes the given fault entry from an entity."""
        ...


    def get_engine_ecu_fault_by_id(
        self,
        fault_id: str,
    ) -> object:
        """Retrieve a specific fault from the engine ECU by its ID."""
        ...


    def get_engine_ecu_faults(
        self,
        scope: str,
    ) -> List[object]:
        """Retrieve faults from the simulated engine ECU. Supports scope filter (active, pending, permanent)."""
        ...


    def get_fault_by_id(
        self,
        entity_collection: str,
        entity_id: str,
        fault_code: str,
        include_schema: bool,
    ) -> GetFaultById200Response:
        """This method provides the details for a fault-code."""
        ...


    def get_faults(
        self,
        entity_collection: str,
        entity_id: str,
        include_schema: bool,
        status_key: str,
        severity: int,
        scope: str,
    ) -> GetFaults200Response:
        """This method provides the fault entries which are detected for an entity, if no query parameter is used. The returned fault entries may be filtered by their status."""
        ...
