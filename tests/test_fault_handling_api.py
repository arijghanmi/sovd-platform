# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.get_fault_by_id200_response import GetFaultById200Response  # noqa: F401
from openapi_server.models.get_faults200_response import GetFaults200Response  # noqa: F401


def test_add_engine_ecu_fault(client: TestClient):
    """Test case for add_engine_ecu_fault

    Add Engine Fault
    """
    body = None

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/ecu/engine/faults",
    #    headers=headers,
    #    json=body,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_clear_engine_ecu_faults(client: TestClient):
    """Test case for clear_engine_ecu_faults

    Clear Engine Faults
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/ecu/engine/faults",
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_all_faults(client: TestClient):
    """Test case for delete_all_faults

    
    """
    params = [("scope", 'scope_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/faults".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_delete_fault_by_id(client: TestClient):
    """Test case for delete_fault_by_id

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/{entity-collection}/{entity-id}/faults/{fault-code}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', fault-code='fault_code_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_fault_by_id(client: TestClient):
    """Test case for get_engine_ecu_fault_by_id

    Get Engine Fault By ID
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/faults/{fault_id}".format(fault_id='fault_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_engine_ecu_faults(client: TestClient):
    """Test case for get_engine_ecu_faults

    Get Engine Faults
    """
    params = [("scope", 'scope_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/ecu/engine/faults",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_fault_by_id(client: TestClient):
    """Test case for get_fault_by_id

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/faults/{fault-code}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', fault-code='fault_code_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_faults(client: TestClient):
    """Test case for get_faults

    
    """
    params = [("include_schema", True),     ("status_key", 'status_key_example'),     ("severity", 56),     ("scope", 'scope_example')]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/faults".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

