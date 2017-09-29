# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from utilities.meta import Meta
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    def test_1(self, graph):
        graph.cypher("MATCH (n) RETURN n")

        return "1"

    def get(self, test_num):

        graph = self.get_service_instance('neo4j')

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_%d" % test_num
        if method_name not in methods:
            raise RestApiException("Test %d not found" % test_num)
        method = methods[method_name]
        out = method(graph)
        return self.force_response(out)
