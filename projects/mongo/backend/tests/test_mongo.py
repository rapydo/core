# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import get_logger

log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
