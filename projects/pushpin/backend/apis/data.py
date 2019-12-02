# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi.decorators import catch_error
from restapi.protocols.bearer import authentication
from restapi.flask_ext.flask_celery import CeleryExt
# from restapi.utilities.logs import log


class Data(EndpointResource):

    POST = {'/data': {'summary': 'Start a data task', 'responses': {'200': {'description': 'Task executed'}}}}

    @catch_error()
    @authentication.required()
    def post(self):
        # celery = self.get_service_instance('celery')

        task = CeleryExt.data_task.apply_async(
            args=[], countdown=5
        )
        return self.force_response(task.task_id)
