# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)
        endpoint = API_URI + '/flat'

        r = client.get(endpoint, data={"test_num": 1})
        assert r.status_code == hcodes.HTTP_OK_BASIC
        assert self.get_content(r) == "1"

        r = client.get(endpoint, data={"test_num": 2})
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND
        assert self.get_content(r) == "Just an error"

        endpoint = API_URI + '/marshal'

        r = client.get(endpoint, data={"test_num": 1})
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert "value" in c
        assert "hideme" not in c
        assert c["value"] == 123

        r = client.get(endpoint, data={"test_num": 2})
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND
        c = self.get_content(r)
        assert "mykey" in c
        # marshal removed this key from the response
        assert "hideme" not in c
        assert c["mykey"] == "Just an error"

        r = client.get(endpoint, data={"test_num": 3})
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        c = self.get_content(r)
        assert "mykey" in c
        # no marshal applied
        assert "hideme" in c
        assert c["mykey"] == "Just an error"
