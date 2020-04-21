# -*- coding: utf-8 -*-

# import time
from restapi.tests import BaseTests, API_URI
# from restapi.utilities.logs import log


class TestApp(BaseTests):

    def test_01_x(self, app, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == 200

        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint)
        assert r.status_code == 200

        task_id = self.get_content(r)
        # We expect as return value the task_id and no more
        assert isinstance(task_id, str)

        celery = self.get_celery(app)
        res = celery.testme()
        assert res == "Task executed!"
