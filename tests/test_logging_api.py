# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_logs_config_get200_response import EntityCollectionEntityIdLogsConfigGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_logs_config_put_request import EntityCollectionEntityIdLogsConfigPutRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_logs_entries_get200_response import EntityCollectionEntityIdLogsEntriesGet200Response  # noqa: F401


def test_clear_engine_ecu_logs(client: TestClient):
    """Test case for clear_engine_ecu_logs

    Clear Engine Diagnostic Logs
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/ecu/engine/logs",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_logs_config_delete(client: TestClient):
    """Test case for entity_collection_entity_id_logs_config_delete

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/logs/config".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_logs_config_get(client: TestClient):
    """Test case for entity_collection_entity_id_logs_config_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/logs/config".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_logs_config_put(client: TestClient):
    """Test case for entity_collection_entity_id_logs_config_put

    
    """
    entity_collection_entity_id_logs_config_put_request = {"items":[{"context":{"type":"RFC5424","host":"Linux","process":"systemd"},"severity":"warn"}]}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/logs/config".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_logs_config_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_logs_entries_get(client: TestClient):
    """Test case for entity_collection_entity_id_logs_entries_get

    
    """
    params = [("severity", 'severity_example'),     ("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/logs/entries".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_logs(client: TestClient):
    """Test case for get_engine_ecu_logs

    Get Engine Diagnostic Logs
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/logs",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

