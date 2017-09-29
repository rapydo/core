# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class TestRestApiException(EndpointResource):

    @catch_error()
    def get(self, test_param):

        if test_param > 0:
            code = int(test_param)
        else:
            code = None
        raise RestApiException("Failed", status_code=code)
