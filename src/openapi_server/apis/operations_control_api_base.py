# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse
from openapi_server.models.entity_collection_entity_id_operations_get200_response import EntityCollectionEntityIdOperationsGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post202_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post_request import EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest
from openapi_server.models.entity_collection_entity_id_operations_operation_id_get200_response import EntityCollectionEntityIdOperationsOperationIdGet200Response


class BaseOperationsControlApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseOperationsControlApi.subclasses = BaseOperationsControlApi.subclasses + (cls,)
    def entity_collection_entity_id_operations_get(
        self,
        entity_collection: str,
        entity_id: str,
        include_proximity_proof: bool,
        include_schema: bool,
    ) -> EntityCollectionEntityIdOperationsGet200Response:
        """This method returns all available operations defined for the given entity."""
        ...


    def entity_collection_entity_id_operations_operation_id_executions_execution_id_delete(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
        execution_id: str,
        entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request: EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest,
    ) -> None:
        """This method terminates the execution of the operation and removes it, and the status of the operation can no longer be requested."""
        ...


    def entity_collection_entity_id_operations_operation_id_executions_execution_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
        execution_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response:
        """This method returns the current status of the operation execution."""
        ...


    def entity_collection_entity_id_operations_operation_id_executions_execution_id_put(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
        execution_id: str,
        entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request: EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest,
    ) -> EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response:
        """This method executes the given capability on the provided operation."""
        ...


    def entity_collection_entity_id_operations_operation_id_executions_get(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
    ) -> EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response:
        """This method returns currently existing executions of the given operation."""
        ...


    def entity_collection_entity_id_operations_operation_id_executions_post(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
        entity_collection_entity_id_operations_operation_id_executions_post_request: EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest,
    ) -> EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response:
        """Start Execution of an Operation An operation may support multiple executions in parallel. If this is not supported, this method will return an error if an operation with the same operation-id is already being executed. A successfully started operation is added to the executions collection if it is executed asynchronously. After the asynchronous execution has been finished, the execution resource remains existent and an SOVD client can receive the status. However, the status of the execution cannot be queried indefinitely as an SOVD server implementation may remove the resource, e.g., upon SOVD server restart."""
        ...


    def entity_collection_entity_id_operations_operation_id_get(
        self,
        entity_collection: str,
        entity_id: str,
        operation_id: str,
        include_schema: bool,
    ) -> EntityCollectionEntityIdOperationsOperationIdGet200Response:
        """This method returns all the details on the specified operation of the given entity."""
        ...
