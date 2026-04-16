# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_operations_operation_id_executions_post200_response_error import EntityCollectionEntityIdOperationsOperationIdExecutionsPost200ResponseError  # noqa: F401
from openapi_server.models.entity_collection_entity_id_updates_get200_response import EntityCollectionEntityIdUpdatesGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_updates_get_origin_parameter import EntityCollectionEntityIdUpdatesGetOriginParameter  # noqa: F401
from openapi_server.models.entity_collection_entity_id_updates_update_package_id_get200_response import EntityCollectionEntityIdUpdatesUpdatePackageIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_updates_update_package_id_status_get200_response import EntityCollectionEntityIdUpdatesUpdatePackageIdStatusGet200Response  # noqa: F401
from openapi_server.models.updates_post201_response import UpdatesPost201Response  # noqa: F401


def test_entity_collection_entity_id_updates_get(client: TestClient):
    """Test case for entity_collection_entity_id_updates_get

    
    """
    params = [("target_version", 'target_version_example'),     ("origin", openapi_server.EntityCollectionEntityIdUpdatesGetOriginParameter())]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/updates".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_automated_put(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_automated_put

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}/automated".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_delete(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_delete

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_execute_put(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_execute_put

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}/execute".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_prepare_put(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_prepare_put

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}/prepare".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_updates_update_package_id_status_get(client: TestClient):
    """Test case for entity_collection_entity_id_updates_update_package_id_status_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/updates/{update-package-id}/status".format(entity-collection='entity_collection_example', entity-id='entity_id_example', update-package-id='update_package_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_update_status(client: TestClient):
    """Test case for get_engine_ecu_update_status

    Get Update Status
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/updates/{update_id}".format(update_id='update_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_updates(client: TestClient):
    """Test case for get_engine_ecu_updates

    Get Available Updates
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/updates",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_initiate_engine_ecu_update(client: TestClient):
    """Test case for initiate_engine_ecu_update

    Initiate Software Update
    """
    body = None

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/ecu/engine/updates",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_updates_post(client: TestClient):
    """Test case for updates_post

    
    """
    body = None

    headers = {
        "content_type": 'content_type_example',
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/updates",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

