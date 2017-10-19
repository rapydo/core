# -*- coding: utf-8 -*-

from restapi.tests import BaseTests
from restapi.tests.utilities import API_URI
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        content = self.get_content(r)
        assert content == "task_id"
