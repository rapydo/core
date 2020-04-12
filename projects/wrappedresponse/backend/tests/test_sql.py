# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)
        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
