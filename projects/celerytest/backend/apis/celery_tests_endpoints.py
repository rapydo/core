# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from utilities.meta import Meta
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    def test_1(self, celery):

        return "1"

    def get(self, test_num):
        celery = self.get_service_instance('celery')

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_%d" % test_num
        if method_name not in methods:
            raise RestApiException("Test %d not found" % test_num)
        method = methods[method_name]
        out = method(celery)
        return self.force_response(out)
