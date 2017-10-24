# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from restapi.flask_ext.flask_celery import CeleryExt
from utilities.meta import Meta
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(EndpointResource):

    def test_1(self, celery, task_id=None):

        # Just test the endpoint is able to retrieve the instance
        return "1"

    def test_2(self, celery, task_id=None):

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
        method_name = "test_%s" % test_num
        if method_name not in methods:
            raise RestApiException("Test %d not found" % test_num)
        method = methods[method_name]
        out = method(celery, task_id)
        return self.force_response(out)
