# -*- coding: utf-8 -*-

"""
An endpoint example
"""

from flask import current_app
from restapi.rest.definition import EndpointResource
# from restapi.services.detect import SQL_AVAILABLE, GRAPHDB_AVAILABLE

from utilities.logs import get_logger

log = get_logger(__name__)


#####################################
if current_app.config['TESTING']:
    class DoTests(EndpointResource):

        def get(self):
            rpc = self.global_get_service('rpc')
            print(rpc)
            log.warning("a call")
            return self.force_response('Hello world!')
