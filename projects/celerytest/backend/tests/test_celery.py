# -*- coding: utf-8 -*-

# import time
from restapi.tests import BaseTests, API_URI
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, app, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        endpoint = API_URI + '/tests/2'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        task_id = self.get_content(r)
        # We expect as return value the task_id and no more
        assert type(task_id) == str

        # endpoint = API_URI + '/tests/3/%s' % task_id
        # wait = 20
        # for count in range(1, 20):
        #     r = client.get(endpoint)
        #     assert r.status_code == HTTP_OK_BASIC

        #     content = self.get_content(r)
        #     assert content['task_id'] == task_id
        #     if content['status'] == "PENDING":
        #         log.print("Task is already pending, sleeping")
        #         time.sleep(wait)
        #         continue
        #     break

        # assert content['status'] == "SUCCESS"
        # assert content['result'] == "Task executed!"

        celery = self.get_celery(app)
        res = celery.testme()
        assert res == "Task executed!"
