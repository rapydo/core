# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi import decorators

from restapi.connectors.celery import CeleryExt
# from restapi.utilities.logs import log


class DoTests(EndpointResource):

    # schema_expose = True
    labels = ['tests']
    GET = {
        '/tests/<test_num><task_id>': {
            'summary': 'Do tests',
            'responses': {'200': {'description': 'a test is executed'}}
        }
    }

    @staticmethod
    def test_1(celery, task_id=None):

        # Just test the endpoint is able to retrieve the instance
        return "1"

    @staticmethod
    def test_2(celery, task_id=None):

        t = "celerybeat.tasks.test_task.testme"

        CeleryExt.create_periodic_task("test", t, every=60)

        CeleryExt.create_crontab_task("test", t, minute=0, hour=3)

        return "1"

    @decorators.catch_errors()
    def get(self, test_num, task_id=None):
        celery = self.get_service_instance('celery')

        if test_num == "1":
            out = self.test_1(celery, task_id)
        elif test_num == "2":
            out = self.test_2(celery, task_id)
        else:
            raise RestApiException("Test {} not found".format(test_num))

        return self.response(out)
