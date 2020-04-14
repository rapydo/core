# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
# from restapi.exceptions import RestApiException
from restapi import decorators
from restapi.utilities.logs import log


class DoTests(EndpointResource):

    labels = ['tests']
    GET = {
        '/tests/<test_num>': {
            'summary': 'Do tests',
            'responses': {'200': {'description': 'a test is executed'}}
        }
    }

    @decorators.catch_errors()
    def get(self, test_num):
        sql = self.get_service_instance('sqlalchemy')

        log.debug(sql)
        return self.response("1")
