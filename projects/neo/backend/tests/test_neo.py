# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)
        headers, _ = self.do_login(client, None, None)

        # Cypher query
        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == 200

        # Wrong cypher query (with syntax error)
        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == 400

        # Nodes and relationships creation, based on models
        endpoint = API_URI + '/tests/3'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == 200

        # Read nodes and relationships created
        endpoint = API_URI + '/tests/4'
        r = client.get(endpoint, headers=headers)
        content = self.get_content(r)
        assert r.status_code == 200
        assert "name" in content
        assert "extra" not in content
        assert "_test2" not in content
        assert "_test1" in content
        assert len(content["_test1"]) > 0
        attrs = content["_test1"][0]
        assert "p_str" in attrs
        assert "p_int" not in attrs
