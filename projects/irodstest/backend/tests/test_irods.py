# -*- coding: utf-8 -*-

from restapi.tests import BaseTests
from restapi.tests.utilities import API_URI
from restapi.services.detect import detector
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        irods = detector.extensions_instances.get('irods')

        home = irods.get_user_home()

        assert home == "test"
