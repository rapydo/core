# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from restapi.utilities.meta import Meta
# from restapi.utilities.logs import log


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    # schema_expose = True
    labels = ['tests']
    GET = {'/tests/<test_num>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}}

    def test_1(self, irods):

        return "1"

    @catch_error()
    def get(self, test_num):
        irods = self.get_service_instance('irods')

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_{}".format(test_num)
        if method_name not in methods:
            raise RestApiException("Test {} not found".format(test_num))
        method = methods[method_name]
        out = method(irods)
        return self.response(out)
