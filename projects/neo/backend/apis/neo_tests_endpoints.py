# -*- coding: utf-8 -*-

"""
An endpoint example
"""

# from flask import current_app
from restapi.rest.definition import EndpointResource
from utilities.meta import Meta
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    def test_1(self):
        print("Mi hai trovato!!")

    def get(self, test_num):

        graph = self.get_service_instance('neo4j')
        print(graph)
        log.warning("a call")
        graph.cypher("MATCH (n) RETURN n")

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        print(methods)
        return self.force_response('Hello world')
