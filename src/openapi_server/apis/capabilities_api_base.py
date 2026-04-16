# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from openapi_server.models.any_path_docs_get_default_response import AnyPathDocsGetDefaultResponse


class BaseCapabilitiesApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseCapabilitiesApi.subclasses = BaseCapabilitiesApi.subclasses + (cls,)
    def any_path_docs_get(
        self,
        any_path: str,
    ) -> object:
        """For entities, resources, and resource collections, a corresponding online capability description can be requested at the SOVD API. The resulting online capability description is a self-contained, valid OpenAPI specification. The description contains information which refers to the creation, reading, updating or deleting of the respective element and its direct child elements as defined by the SOVD standard. An online capability description is requested for a data resource /{entity-path}/data/{data-id} via GET /{entity-path}/data/{data-id}/docs. For example, to enrich the responses with additional details such as the underlying schema of the response using the “include-schema” query parameter on the request. Moreover, for each supported HTTP method all defined HTTP response status codes are documented together with the data model of the resulting response payloads."""
        ...
