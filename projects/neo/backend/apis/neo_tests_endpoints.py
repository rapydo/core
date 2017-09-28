# -*- coding: utf-8 -*-

"""
An endpoint example
"""

from restapi.rest.definition import EndpointResource
# from restapi.services.detect import SQL_AVAILABLE, GRAPHDB_AVAILABLE

from utilities.logs import get_logger

log = get_logger(__name__)


class DoTests(EndpointResource):

    def get(self):

        user = self.get_current_user()
        graph = self.global_get_service('neo4j')
        print(graph)
        log.warning("a call")
        return self.force_response('Hello world, %s!' % user)
