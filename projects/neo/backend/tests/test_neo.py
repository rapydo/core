# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
# from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        headers, _ = self.do_login(client, None, None)

        # Cypher query
        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == hcodes.HTTP_OK_BASIC

        # Wrong cypher query (with syntax error)
        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == hcodes.HTTP_BAD_REQUEST

        # Nodes and relationships creation, based on models
        endpoint = API_URI + '/tests/3'
        r = client.get(endpoint, headers=headers)
        assert r.status_code == hcodes.HTTP_OK_BASIC

        # Read nodes and relationships created
        endpoint = API_URI + '/tests/4'
        r = client.get(endpoint, headers=headers)
        content = self.get_content(r)
        assert r.status_code == hcodes.HTTP_OK_BASIC
        assert "attributes" in content
        assert "name" in content["attributes"]
        assert "extra" not in content["attributes"]
        assert "relationships" in content
        assert "test2" not in content["relationships"]
        assert "test1" in content["relationships"]
        assert len(content["relationships"]["test1"]) > 0
        assert "attributes" in content["relationships"]["test1"][0]
        attrs = content["relationships"]["test1"][0]["attributes"]
        assert "p_str" in attrs
        assert "p_int" not in attrs
