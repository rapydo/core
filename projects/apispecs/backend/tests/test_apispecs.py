# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)
        endpoint = API_URI + '/tests'

        r = client.get(endpoint, "", {"test_num": 1})
        assert r.status_code == hcodes.HTTP_OK_BASIC
        assert self.get_content(r) == "1"

        r = client.get(endpoint, "", {"test_num": 2})
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND
        assert self.get_content(r) == "Just an error"