# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.areas_area_id_related_components_get200_response import AreasAreaIdRelatedComponentsGet200Response  # noqa: F401
from openapi_server.models.entity_collection_entity_id_get200_response import EntityCollectionEntityIdGet200Response  # noqa: F401
from openapi_server.models.entity_collection_get200_response import EntityCollectionGet200Response  # noqa: F401


def test_areas_area_id_related_components_get(client: TestClient):
    """Test case for areas_area_id_related_components_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/areas/{area-id}/related-components".format(area-id='area_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_areas_area_id_subareas_get(client: TestClient):
    """Test case for areas_area_id_subareas_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/areas/{area-id}/subareas".format(area-id='area_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_components_component_id_related_apps_get(client: TestClient):
    """Test case for components_component_id_related_apps_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/components/{component-id}/related-apps".format(component-id='component_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_components_component_id_subcomponents_get(client: TestClient):
    """Test case for components_component_id_subcomponents_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/components/{component-id}/subcomponents".format(component-id='component_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_entity_id_get(client: TestClient):
    """Test case for entity_collection_entity_id_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_entity_collection_get(client: TestClient):
    """Test case for entity_collection_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}".format(entity-collection='entity_collection_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

