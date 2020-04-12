# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi import decorators
from restapi.connectors.celery import CeleryExt
# from restapi.utilities.logs import log


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    # schema_expose = True
    labels = ['tests']
    GET = {'/tests/<int:test_num>/<task_id>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}, '/tests/<test_num>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}}

    @staticmethod
    def test_1(celery, task_id=None):

        # Just test the endpoint is able to retrieve the instance
        return "1"

    def test_2(self, celery, task_id=None):

        rabbit = self.get_service_instance('rabbit')

        rabbit.write_to_queue("test", "celery")

        task = CeleryExt.testme.apply_async(
            args=[]
        )
        # task = CeleryExt.testme.apply_async(
        #     args=[], countdown=1
        # )
        # task = CeleryExt.priotestme.testme(
        #     args=[], priority=8
        # )

        return task.id

    @staticmethod
    def test_3(celery, task_id=None):

        task = celery.AsyncResult(task_id)
        if task is None:
            return None

        return {
            "task_id": task.task_id,
            "status": task.status,
            "result": task.result
        }

    @decorators.catch_errors()
    def get(self, test_num, task_id=None):
        celery = self.get_service_instance('celery')

        if test_num == "1":
            out = self.test_1(celery, task_id)
        elif test_num == "2":
            out = self.test_2(celery, task_id)
        elif test_num == "3":
            out = self.test_3(celery, task_id)
        else:
            raise RestApiException("Test {} not found".format(test_num))

        return self.response(out)
