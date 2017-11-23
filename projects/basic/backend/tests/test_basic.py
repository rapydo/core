# -*- coding: utf-8 -*-

import pytest
from restapi.tests import BaseTests, API_URI
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.htmlcodes import HTTP_SERVER_ERROR
from utilities.htmlcodes import HTTP_BAD_NOTFOUND
from utilities.htmlcodes import HTTP_BAD_REQUEST
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        endpoint = API_URI + '/basic_tests/restapi/0'
        r = client.get(endpoint)
        assert r.status_code == HTTP_BAD_NOTFOUND

        endpoint = API_URI + '/basic_tests/restapi/378'
        r = client.get(endpoint)
        assert r.status_code == HTTP_SERVER_ERROR

        endpoint = '%s/basic_tests/restapi/%s' % (API_URI, HTTP_OK_BASIC)
        r = client.get(endpoint)
        assert r.status_code == HTTP_SERVER_ERROR

        endpoint = '%s/basic_tests/restapi/%s' % (API_URI, HTTP_BAD_REQUEST)
        r = client.get(endpoint)
        assert r.status_code == HTTP_BAD_REQUEST

        k = "test_save"
        v = "This is the test value"

        self.save(k, v)
        assert v == self.get(k)
        try:
            self.get("this_key_does_notexists")
        except AttributeError:
            pass
        else:
            pytest.fail("This call should raise an AttributeError, why not???")
