# coding: utf-8

from fastapi.testclient import TestClient


from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse  # noqa: F401


def test_any_path_docs_get(client: TestClient):
    """Test case for any_path_docs_get

    
    """

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/{any-path}/docs".format(any-path='any_path_example'),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

