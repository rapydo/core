# -*- coding: utf-8 -*-

from restapi.tests import BaseTests
from restapi.tests.utilities import API_URI
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.htmlcodes import HTTP_BAD_REQUEST
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        headers, _ = self.do_login(client, None, None)

        # Cypher query
        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == HTTP_OK_BASIC

        # Wrong cypher query (with syntax error)
        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == HTTP_BAD_REQUEST

        # Nodes and relationships creation, based on models
        endpoint = API_URI + '/tests/3'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == HTTP_OK_BASIC
