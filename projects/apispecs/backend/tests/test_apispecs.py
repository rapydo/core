# -*- coding: utf-8 -*-

from restapi.tests import BaseTests, API_URI
from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, client):

        log.debug("Executing tests from {}", self.__class__.__module__)

        header, _ = self.do_login(client, None, None)

        # Starting from an empty list
        endpoint = API_URI + '/data'
        r = client.get(endpoint, headers=header)
        assert r.status_code == 200
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 0

        # Trying to create an entity, but input is wrong
        r = client.post(endpoint, data={}, headers=header)
        assert r.status_code == 400
        c = self.get_content(r)
        assert "name" in c
        assert "age" in c
        assert "date" in c
        assert "email" in c
        assert "blood_type" in c
        assert "HGB" in c
        # This is optional
        assert "healthy" not in c
        assert c["name"][0] == "Missing data for required field."
        assert c["age"][0] == "Missing data for required field."
        assert c["date"][0] == "Missing data for required field."
        assert c["email"][0] == "Missing data for required field."
        assert c["blood_type"][0] == "Missing data for required field."
        assert c["HGB"][0] == "Missing data for required field."

        # Trying to create an entity, but input is still wrong
        r = client.post(
            endpoint,
            data={
                "name": "x",
                "age": "a",
                "date": "y",
                "email": "w",
                "blood_type": "C+",
                "HGB": "z"
            },
            headers=header
        )
        assert r.status_code == 400
        c = self.get_content(r)
        assert "name" in c
        assert "age" in c
        assert "date" in c
        assert "email" in c
        assert "blood_type" in c
        assert "HGB" in c
        # This is optional
        assert "healthy" not in c
        assert c["name"][0] == "Shorter than minimum length 3."
        assert c["age"][0] == "Not a valid integer."
        assert c["date"][0] == "Not a valid date."
        assert c["email"][0] == "Not a valid email address."
        assert c["blood_type"][0] == "Must be one of: 0+, A+, B+, AB+, 0-, A-, B-, AB-."
        assert c["HGB"][0] == "Not a valid number."

        # Trying to create an entity, but some inputs is still wrong
        r = client.post(
            endpoint,
            data={
                "name": "xyw",
                "age": 9999,
                "date": "1970-01-01T00:00:00.000Z",
                "email": "user@nomail.org",
                "blood_type": "0+",
                "HGB": "-5"
            },
            headers=header
        )
        assert r.status_code == 400
        c = self.get_content(r)
        assert "name" not in c
        assert "age" in c
        assert "date" not in c
        assert "email" not in c
        assert "blood_type" not in c
        assert "HGB" in c
        # This is optional
        assert "healthy" not in c
        assert c["age"][0] == "Must be greater than or equal to 18 and less than or equal to 99."
        assert c["HGB"][0] == "Must be greater than or equal to 0 and less than or equal to 30."

        # Creating an entity and retrieving the corresponding uuid
        r = client.post(
            endpoint,
            data={
                "name": "xyw",
                "age": 18,
                "date": "1970-01-01T00:00:00.000Z",
                "email": "user@nomail.org",
                "blood_type": "0+",
                "HGB": "15.3",
            },
            headers=header
        )
        assert r.status_code == 200
        c = self.get_content(r)
        assert "name" not in c
        assert "age" not in c
        assert "date" not in c
        assert "email" not in c
        assert "blood_type" not in c
        assert "HGB" not in c

        uuid = c

        # Verify the newly created entity
        r = client.get(endpoint, headers=header)
        assert r.status_code == 200
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 1
        assert c[0]['uuid'] == uuid
        assert c[0]['name'] == "xyw"
        assert c[0]['age'] == 18
        assert c[0]['date'] == "1970-01-01T00:00:00.000Z"
        assert c[0]['email'] == "user@nomail.org"
        assert c[0]['blood_type'] == "0+"
        assert c[0]['HGB'] == 15.3
        # Healthy defaulted to True
        assert c[0]['healthy']

        # Trying to modify a non existing entity
        r = client.put(endpoint + "/xyz", headers=header)
        assert r.status_code == 404

        # Modifying an entity, note that email will not change
        r = client.put(
            endpoint + "/" + uuid,
            data={
                "name": "abc",
                "email": "nomail@user.org"
            },
            headers=header
        )
        assert r.status_code == 204

        # Verify that entity is changed
        r = client.get(endpoint, headers=header)
        assert r.status_code == 200
        c = self.get_content(r)
        assert c[0]['uuid'] == uuid
        # name is changed
        assert c[0]['name'] == "abc"
        # email is not changed
        assert c[0]['email'] == "user@nomail.org"

        # cannot delete non existing entities
        r = client.delete(endpoint + "/xyz", headers=header)
        assert r.status_code == 404

        # entity is now deleted
        r = client.delete(endpoint + "/" + uuid, headers=header)
        assert r.status_code == 204

        # cannot delete entity already deleted
        r = client.delete(endpoint + "/" + uuid, headers=header)
        assert r.status_code == 404

        # data list is now empty again
        r = client.get(endpoint, headers=header)
        assert r.status_code == 200
        c = self.get_content(r)
        assert isinstance(c, list)
        assert len(c) == 0
