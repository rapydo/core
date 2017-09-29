# -*- coding: utf-8 -*-

"""
An endpoint example
"""

# from flask import current_app
from restapi.rest.definition import EndpointResource

from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class SqlEndPoint(EndpointResource):

    def get(self):
        sql = self.get_service_instance('sql')
        print(sql)
        log.warning("a call")
        return self.force_response('Hello world!')
