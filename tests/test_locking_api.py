# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_locks_get200_response import EntityCollectionEntityIdLocksGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_locks_lock_id_get200_response import EntityCollectionEntityIdLocksLockIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_locks_post201_response import EntityCollectionEntityIdLocksPost201Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_locks_post_request import EntityCollectionEntityIdLocksPostRequest  # noqa: F401


def test_entity_collection_entity_id_locks_get(client: TestClient):
    """Test case for entity_collection_entity_id_locks_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/locks".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_locks_lock_id_delete(client: TestClient):
    """Test case for entity_collection_entity_id_locks_lock_id_delete

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/locks/{lock-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', lock-id='lock_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_locks_lock_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_locks_lock_id_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/locks/{lock-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', lock-id='lock_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_locks_lock_id_put(client: TestClient):
    """Test case for entity_collection_entity_id_locks_lock_id_put

    
    """
    entity_collection_entity_id_locks_post_request = openapi_server.EntityCollectionEntityIdLocksPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/locks/{lock-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', lock-id='lock_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_locks_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_locks_post(client: TestClient):
    """Test case for entity_collection_entity_id_locks_post

    
    """
    entity_collection_entity_id_locks_post_request = openapi_server.EntityCollectionEntityIdLocksPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{entity-collection}/{entity-id}/locks".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_locks_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

