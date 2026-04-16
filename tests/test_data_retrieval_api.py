# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_categories_get200_response import EntityCollectionEntityIdDataCategoriesGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response import EntityCollectionEntityIdDataDataIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response_errors_inner import EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_data_id_put_request import EntityCollectionEntityIdDataDataIdPutRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_get200_response import EntityCollectionEntityIdDataGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_groups_get200_response import EntityCollectionEntityIdDataGroupsGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_lists_data_list_id_get200_response import EntityCollectionEntityIdDataListsDataListIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_lists_post201_response import EntityCollectionEntityIdDataListsPost201Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_lists_post_request import EntityCollectionEntityIdDataListsPostRequest  # noqa: F401
from openapi_server.models.get_engine_ecu_speed200_response import GetEngineEcuSpeed200Response  # noqa: F401


def test_entity_collection_entity_id_data_categories_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_categories_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data-categories".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_data_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_data_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data/{data-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', data-id='data_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_data_id_put(client: TestClient):
    """Test case for entity_collection_entity_id_data_data_id_put

    
    """
    entity_collection_entity_id_data_data_id_put_request = openapi_server.EntityCollectionEntityIdDataDataIdPutRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/data/{data-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', data-id='data_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_data_data_id_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_get

    
    """
    params = [("groups", 'groups_example'),     ("category", ['category_example']),     ("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_groups_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_groups_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data-groups".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_lists_data_list_id_delete(client: TestClient):
    """Test case for entity_collection_entity_id_data_lists_data_list_id_delete

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/data-lists/{data-list-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', data-list-id='data_list_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_lists_data_list_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_lists_data_list_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data-lists/{data-list-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', data-list-id='data_list_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_lists_get(client: TestClient):
    """Test case for entity_collection_entity_id_data_lists_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/data-lists".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_data_lists_post(client: TestClient):
    """Test case for entity_collection_entity_id_data_lists_post

    
    """
    entity_collection_entity_id_data_lists_post_request = openapi_server.EntityCollectionEntityIdDataListsPostRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/{entity-collection}/{entity-id}/data-lists".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_data_lists_post_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_data(client: TestClient):
    """Test case for get_engine_ecu_data

    Get All ECU Data
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/data",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_data_by_id(client: TestClient):
    """Test case for get_engine_ecu_data_by_id

    Get ECU Data By ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/data/{data_id}".format(data_id='data_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_speed(client: TestClient):
    """Test case for get_engine_ecu_speed

    Get Vehicle Speed
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/data/speed",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_speed_events(client: TestClient):
    """Test case for get_engine_ecu_speed_events

    SSE - Speed ResponseOnEvent
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/data/speed/events",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_update_engine_ecu_data(client: TestClient):
    """Test case for update_engine_ecu_data

    Update ECU Data
    """
    body = None

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/ecu/engine/data/{data_id}".format(data_id='data_id_example'),
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

