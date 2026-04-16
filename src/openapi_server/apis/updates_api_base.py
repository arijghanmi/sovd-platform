# coding: utf-8

from typing import Optional, Any, ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post200_response_error import EntityCollectionEntityIdOperationsOperationIdExecutionsPost200ResponseError
from openapi_server.models.entity_collection_entity_id_updates_get200_response import EntityCollectionEntityIdUpdatesGet200Response
from openapi_server.models.entity_collection_entity_id_updates_get_origin_parameter import EntityCollectionEntityIdUpdatesGetOriginParameter
from openapi_server.models.entity_collection_entity_id_updates_update_package_id_get200_response import EntityCollectionEntityIdUpdatesUpdatePackageIdGet200Response
from openapi_server.models.entity_collection_entity_id_updates_update_package_id_status_get200_response import EntityCollectionEntityIdUpdatesUpdatePackageIdStatusGet200Response
from openapi_server.models.updates_post201_response import UpdatesPost201Response


class BaseUpdatesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseUpdatesApi.subclasses = BaseUpdatesApi.subclasses + (cls,)
    def entity_collection_entity_id_updates_get(
        self,
        entity_collection: str,
        entity_id: str,
        target_version: str,
        origin: EntityCollectionEntityIdUpdatesGetOriginParameter,
    ) -> EntityCollectionEntityIdUpdatesGet200Response:
        """The method returns the available updates for the entity."""
        ...


    def entity_collection_entity_id_updates_update_package_id_automated_put(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
    ) -> None:
        """The method starts the automated installation of the update package. For this scenario, the SOVD server and the OEM’s backend have full control over the update process and decide which action can be taken when. The method returns immediately and redirects the SOVD client to a method for requesting the status and progress of the installation."""
        ...


    def entity_collection_entity_id_updates_update_package_id_delete(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
    ) -> None:
        """The method deletes an update package from SOVD server. The resource is afterwards not available anymore."""
        ...


    def entity_collection_entity_id_updates_update_package_id_execute_put(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
    ) -> None:
        """The method starts the installation and activation of the update package. As part of this step the following tasks are performed for example:   - Validation if the update package is still installable (e.g., checking the software versions of the updated entities)   - Installation of the update on all updated entities   - Configuration of the entities   - Execution of specific post install actions   - Activation of the update (e.g., by switching to B-memory)   - Rollback of update in case of an error  The method returns immediately and redirects the SOVD client to a method for requesting the status and progress of the installation. After the update has been finished, the resource for the update package (and its sub-resources like status) remains existent and an SOVD client can receive the status of an update package. However, the status of the update package cannot be queried indefinitely as an SOVD server implementation may remove the update package resource, e.g., upon SOVD server restart or the retrieval of new update packages."""
        ...


    def entity_collection_entity_id_updates_update_package_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdUpdatesUpdatePackageIdGet200Response:
        """The method returns detailed information for a given update package."""
        ...


    def entity_collection_entity_id_updates_update_package_id_prepare_put(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
    ) -> None:
        """The method starts the preparation of the update package for installation. As part of this step the following tasks are performed for example:   - Validates if the update package is still installable (e.g., checking the software versions of the affected entities)   - Download of update package from OTA backend   - Validation of the integrity of update package   - Applying deltas   - Installing the update in B-memory  The method returns immediately and redirects the SOVD client to a method for requesting the status and progress of the preparation. An SOVD server may remove prepared updates after an OEM defined amount of time. An explicit removal of a prepared update by an SOVD client is not provided by the SOVD API as the update is implicitly removed after installation. If an update fails, it is in general not implicitly removed as the prepared package may be used for anoth"""
        ...


    def entity_collection_entity_id_updates_update_package_id_status_get(
        self,
        entity_collection: str,
        entity_id: str,
        update_package_id: str,
    ) -> EntityCollectionEntityIdUpdatesUpdatePackageIdStatusGet200Response:
        """The method returns the status of the preparation or execution of the update."""
        ...


    def get_engine_ecu_update_status(
        self,
        update_id: str,
    ) -> object:
        """Check the status of a software update for the engine ECU."""
        ...


    def get_engine_ecu_updates(
        self,
    ) -> List[object]:
        """List available software update packages for the engine ECU."""
        ...


    def initiate_engine_ecu_update(
        self,
        body: Optional[Any] = None,
    ) -> None:
        """Start a software update process for the engine ECU."""
        ...


    def updates_post(
        self,
        content_type: str,
        body: Optional[Any] = None,
    ) -> UpdatesPost201Response:
        """The method registers a new update at the SOVD server which can be installed afterwards. After creating the update, the SOVD client has to use the methods described before for installing the update (automated or prepare &amp; execute)."""
        ...
