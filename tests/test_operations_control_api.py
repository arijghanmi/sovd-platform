# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_get200_response import EntityCollectionEntityIdOperationsGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request import EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_get200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post200_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post202_response import EntityCollectionEntityIdOperationsOperationIdExecutionsPost202Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post_request import EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_get200_response import EntityCollectionEntityIdOperationsOperationIdGet200Response  # noqa: F401


def test_entity_collection_entity_id_operations_get(client: TestClient):
    """Test case for entity_collection_entity_id_operations_get

    
    """
    params = [("include_proximity_proof", True),     ("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/operations".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_executions_execution_id_delete(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_executions_execution_id_delete

    
    """
    entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request = openapi_server.EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdDeleteRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example', execution-id='execution_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_operations_operation_id_executions_execution_id_delete_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_executions_execution_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_executions_execution_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example', execution-id='execution_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_executions_execution_id_put(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_executions_execution_id_put

    
    """
    entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request = openapi_server.EntityCollectionEntityIdOperationsOperationIdExecutionsExecutionIdPutRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions/{execution-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example', execution-id='execution_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_operations_operation_id_executions_execution_id_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_executions_get(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_executions_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_executions_post(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_executions_post

    
    """
    entity_collection_entity_id_operations_operation_id_executions_post_request = openapi_server.EntityCollectionEntityIdOperationsOperationIdExecutionsPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}/executions".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_operations_operation_id_executions_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_operations_operation_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_operations_operation_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/operations/{operation-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', operation-id='operation_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

