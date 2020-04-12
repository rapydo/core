# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
# from restapi.exceptions import RestApiException
from restapi import decorators
from restapi.utilities.logs import log


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    # schema_expose = True
    labels = ['tests']
    GET = {'/tests/<test_num>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}}

    def test_1(self, mongo):

        return "1"

    @decorators.catch_errors()
    def get(self, test_num):
        mongo = self.get_service_instance('mongo')

        log.debug(mongo)

        return self.response("1")
