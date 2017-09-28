# -*- coding: utf-8 -*-

from tests import RestTestsBase
from restapi.tests.utilities import TestUtilities
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class BaseTests(RestTestsBase, TestUtilities):

    def test_01_x(self):

        # Check success
        endpoint = self._api_uri + '/tests'
        log.info("*** VERIFY if API is online")
        r = self.app.get(endpoint)
        self.assertEqual(r.status_code, self._hcodes.HTTP_OK_BASIC)
