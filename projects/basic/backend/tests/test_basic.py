# -*- coding: utf-8 -*-

from tests import RestTestsBase
from restapi.tests.utilities import TestUtilities
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class BaseTests(RestTestsBase, TestUtilities):

    def test_01_x(self):

        endpoint = self._api_uri + '/basic_tests/restapi/0'
        r = self.app.get(endpoint)
        self.assertEqual(r.status_code, self._hcodes.HTTP_BAD_REQUEST)

        endpoint = self._api_uri + '/basic_tests/restapi/378'
        r = self.app.get(endpoint)
        self.assertEqual(r.status_code, 378)

        ok = self._hcodes.HTTP_OK_BASIC
        endpoint = self._api_uri + '/basic_tests/restapi/%s' % ok
        r = self.app.get(endpoint)
        self.assertEqual(r.status_code, ok)
