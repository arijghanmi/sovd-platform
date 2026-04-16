# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_configurations_configuration_id_put_request import EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest  # noqa: F401
from openapi_server.models.entity_collection_entity_id_configurations_get200_response import EntityCollectionEntityIdConfigurationsGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_data_id_get200_response_errors_inner import EntityCollectionEntityIdDataDataIdGet200ResponseErrorsInner  # noqa: F401
from openapi_server.models.entity_collection_entity_id_data_lists_data_list_id_get200_response_items_inner import EntityCollectionEntityIdDataListsDataListIdGet200ResponseItemsInner  # noqa: F401


def test_entity_collection_entity_id_configurations_configuration_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_configurations_configuration_id_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/configurations/{configuration-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', configuration-id='configuration_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_configurations_configuration_id_put(client: TestClient):
    """Test case for entity_collection_entity_id_configurations_configuration_id_put

    
    """
    entity_collection_entity_id_configurations_configuration_id_put_request = openapi_server.EntityCollectionEntityIdConfigurationsConfigurationIdPutRequest()

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/{entity-collection}/{entity-id}/configurations/{configuration-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example', configuration-id='configuration_id_example'),
    #    headers=headers,
    #    json=entity_collection_entity_id_configurations_configuration_id_put_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_configurations_get(client: TestClient):
    """Test case for entity_collection_entity_id_configurations_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/configurations".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

