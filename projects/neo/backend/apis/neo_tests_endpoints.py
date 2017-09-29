# -*- coding: utf-8 -*-

"""
An endpoint example
"""

# from flask import current_app
from restapi.rest.definition import EndpointResource

from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    def get(self):

        graph = self.get_service_instance('neo4j')
        print(graph)
        log.warning("a call")
        graph.cypher("MATCH (n) RETURN n")
        return self.force_response('Hello world')
