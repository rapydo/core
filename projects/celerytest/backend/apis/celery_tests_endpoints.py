# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from restapi.flask_ext.flask_celery import CeleryExt
from restapi.utilities.meta import Meta
# from restapi.utilities.logs import log


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    # schema_expose = True
    labels = ['tests']
    GET = {'/tests/<test_num>/<task_id>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}, '/tests/<test_num>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}}

    def test_1(self, celery, task_id=None):

        # Just test the endpoint is able to retrieve the instance
        return "1"

    def test_2(self, celery, task_id=None):

        rabbit = self.get_service_instance('rabbit')

        rabbit.write_to_queue("test", "celery")

        task = CeleryExt.testme.apply_async(
            args=[], countdown=0
        )
        return task.id

    def test_3(self, celery, task_id=None):

        task = celery.AsyncResult(task_id)
        if task is None:
            return None

        return {
            "task_id": task.task_id,
            "status": task.status,
            "result": task.result
        }

    @catch_error()
    def get(self, test_num, task_id=None):
        celery = self.get_service_instance('celery')

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_{}".format(test_num)
        if method_name not in methods:
            raise RestApiException("Test {} not found".format(test_num))
        method = methods[method_name]
        out = method(celery, task_id)
        return self.response(out)
