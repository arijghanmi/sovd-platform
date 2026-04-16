# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401
from openapi_server.models.entity_collection_entity_id_bulk_data_get200_response import EntityCollectionEntityIdBulkDataGet200Response  # noqa: F401


def test_entity_collection_entity_id_bulk_data_get(client: TestClient):
    """Test case for entity_collection_entity_id_bulk_data_get

    
    """
    params = [("include_schema", True)]
    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{entity-collection}/{entity-id}/bulk-data".format(entity-collection='entity_collection_example', entity-id='entity_id_example'),
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

