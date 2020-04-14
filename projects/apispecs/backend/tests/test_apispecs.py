# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)
        endpoint = API_URI + '/flat'

        r = client.get(endpoint)
        assert r.status_code == 422

        r = client.get(endpoint, data={"test_num": 1})
        assert r.status_code == hcodes.HTTP_OK_BASIC
        assert self.get_content(r) == "1"

        r = client.get(endpoint, data={"test_num": 2})
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND
        assert self.get_content(r) == "Just an error"

        endpoint = API_URI + '/marshal'

        r = client.get(endpoint)
        assert r.status_code == 422

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

        # Starting from an empty list
        endpoint = API_URI + '/data'
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 0

        # Trying to create an entity, but input is wrong
        r = client.post(endpoint, data={})
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        c = self.get_content(r)
        assert "name" in c
        assert "age" in c
        assert "date" in c
        assert "email" in c
        assert "hgb" in c
        # This is optional
        assert "healthy" not in c
        assert c["name"] == "Missing data for required field."
        assert c["age"] == "Missing data for required field."
        assert c["date"] == "Missing data for required field."
        assert c["email"] == "Missing data for required field."
        assert c["hgb"] == "Missing data for required field."

        # Trying to create an entity, but input is still wrong
        r = client.post(
            endpoint,
            data={
                "name": "x",
                "age": 1,
                "date": "y",
                "email": "w",
                "hgb": "z"
            }
        )
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        c = self.get_content(r)
        assert "name" in c
        assert "age" in c
        assert "date" in c
        assert "email" in c
        assert "hgb" in c
        # This is optional
        assert "healthy" not in c
        assert c["name"] == "Shorter than minimum length 4."
        assert c["age"] == "Not a valid integer."
        assert c["date"] == "Not a valid date."
        assert c["email"] == "Not a valid email address."
        assert c["hgb"] == "Not a valid number."

		# Trying to create an entity, but some inputs is still wrong
        r = client.post(
            endpoint,
            data={
                "name": "xywz",
                "age": 9999,
                "date": "1970-01-01",
                "email": "user@nomail.org",
                "hgb": "-5"
            }
        )
        assert r.status_code == hcodes.HTTP_BAD_REQUEST
        c = self.get_content(r)
        assert "name" not in c
        assert "age" in c
        assert "date" not in c
        assert "email" not in c
        assert "hgb" in c
        # This is optional
        assert "healthy" not in c
        assert c["age"] == "Must be greater than or equal to 18 and less than or equal to 99."
        assert c["hgb"] == "Must be greater than or equal to 0 and less than or equal to 30."

        # Creating an entity and retrieving the corresponding uuid
        r = client.post(
            endpoint,
            data={
                "name": "xywz",
                "age": 18,
                "date": "1970-01-01",
                "email": "user@nomail.org",
                "hgb": "15.3",
            }
        )
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert "name" not in c
        assert "age" not in c
        assert "date" not in c
        assert "email" not in c
        assert "hgb" not in c

        uuid = c

        # Verify the newly created entity
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 1
        assert c[0]['uuid'] == uuid
        assert c[0]['name'] == "xywz"
        assert c[0]['age'] == 18
        assert c[0]['date'] == "1970-01-01"
        assert c[0]['email'] == "user@nomail.org"
        assert c[0]['hgb'] == 15.3
        # Healthy defaulted to True
        assert c[0]['healthy']

        # Trying to modify a non existing entity
        client.put(endpoint + "/xyz")
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND

        # Modifying an entity, note that email will not change
        client.put(
            endpoint + "/" + uuid,
            data={
                "name": "abcd",
                "email": "nomail@user.org"
            }
        )
        assert r.status_code == hcodes.HTTP_OK_NORESPONSE

        # Verify that entity is changed
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert c[0]['uuid'] == uuid
        # name is changed
        assert c[0]['name'] == "abcd"
        # email is not changed
        assert c[0]['email'] == "user@nomail.org"

        # cannot delete non existing entities
        client.delete(endpoint + "/xyz")
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND

        # entity is now deleted
        client.delete(endpoint + "/" + uuid)
        assert r.status_code == hcodes.HTTP_OK_NORESPONSE

        # cannot delete entity already deleted
        client.delete(endpoint + "/" + uuid)
        assert r.status_code == hcodes.HTTP_BAD_NOTFOUND

        # data list is now empty again
        r = client.get(endpoint)
        assert r.status_code == hcodes.HTTP_OK_BASIC
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 0
