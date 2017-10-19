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

        task_id = self.get_content(r)
        # We expect as return value the task_id and no more
        assert type(task_id) == str

        endpoint = API_URI + '/tests/3/%s' % task_id
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        content = self.get_content(r)
        assert content['task_id'] == task_id
        assert content['status'] == "SUCCESS"
        assert content['result'] == "Task executed!"
        assert content['status'] == "STOP ME"

        # VERIFY BATCH ACTIVE
        # for count in range(1, 10):
        #     active = []
        #     active.append(
        #         self._test_get(
        #             batch_def, 'batch/' + study, headers,
        #             OK, parse_response=False
        #         )
        #     )

        #     if len(active) > 0:
        #         wait = 10
        #         print(
        #             "Found %s active operation(s), waiting for %s seconds" %
        #              (len(active), wait)
        #         )
        #         time.sleep(wait)
        #     print("No active operation found, tests can continue")
        #     break
