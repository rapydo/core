# -*- coding: utf-8 -*-

"""
An endpoint example
"""

from restapi.rest.definition import EndpointResource
# from restapi.services.detect import SQL_AVAILABLE, GRAPHDB_AVAILABLE

from utilities.logs import get_logger

log = get_logger(__name__)


#####################################
class DoTests(EndpointResource):

    def get(self):
        log.warning("Received a test HTTP request")
        return self.force_response('Hello world!')
