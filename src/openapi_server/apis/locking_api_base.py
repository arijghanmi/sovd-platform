# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_locks_get200_response import EntityCollectionEntityIdLocksGet200Response
from openapi_server.models.entity_collection_entity_id_locks_lock_id_get200_response import EntityCollectionEntityIdLocksLockIdGet200Response
from openapi_server.models.entity_collection_entity_id_locks_post201_response import EntityCollectionEntityIdLocksPost201Response
from openapi_server.models.entity_collection_entity_id_locks_post_request import EntityCollectionEntityIdLocksPostRequest


class BaseLockingApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseLockingApi.subclasses = BaseLockingApi.subclasses + (cls,)
    def entity_collection_entity_id_locks_get(
        self,
        entity_collection: str,
        entity_id: str,
    ) -> EntityCollectionEntityIdLocksGet200Response:
        """The method returns the acquired locks for the given entity."""
        ...


    def entity_collection_entity_id_locks_lock_id_delete(
        self,
        entity_collection: str,
        entity_id: str,
        lock_id: str,
    ) -> None:
        """This method releases an acquired lock by deleting the created lock resource."""
        ...


    def entity_collection_entity_id_locks_lock_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        lock_id: str,
    ) -> EntityCollectionEntityIdLocksLockIdGet200Response:
        """The method returns all the details on the specified lock of the given entity. For extending the expiration of a lock the method described in 6.11.5 has to be invoked."""
        ...


    def entity_collection_entity_id_locks_lock_id_put(
        self,
        entity_collection: str,
        entity_id: str,
        lock_id: str,
        entity_collection_entity_id_locks_post_request: EntityCollectionEntityIdLocksPostRequest,
    ) -> None:
        """This method extends an acquired lock by providing a new expiration time. The extension is only valid for the SOVD client that has already acquired the corresponding lock."""
        ...


    def entity_collection_entity_id_locks_post(
        self,
        entity_collection: str,
        entity_id: str,
        entity_collection_entity_id_locks_post_request: EntityCollectionEntityIdLocksPostRequest,
    ) -> EntityCollectionEntityIdLocksPost201Response:
        """This method acquires a lock from the SOVD server for the given entity to reserve its resources for exclusive access of a single SOVD client, i.e., prevent other SOVD clients from operating on the resources in parallel. Any further requests against the SOVD API towards controlling an operation (actuators, routines, and input control), e.g., start the execution of an operation, is rejected by the SOVD server if the required lock is not acquired by the same SOVD client. Once the lock is not required anymore, the SOVD client can delete the created lock resource by a corresponding DELETE request. In addition, an SOVD client shall provide a relative expiration time after which the SOVD server should release the lock automatically. The SOVD server might reject the requested expiration time if it is too long. As a result, the SOVD server deletes the corresponding lock resource."""
        ...
