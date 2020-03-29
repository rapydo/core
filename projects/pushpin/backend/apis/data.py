# -*- coding: utf-8 -*-

# from flask import current_app
from restapi.rest.definition import EndpointResource
from restapi import decorators
from restapi.connectors.celery import CeleryExt
# from restapi.utilities.logs import log


class Data(EndpointResource):

    POST = {'/data': {'summary': 'Start a data task', 'responses': {'200': {'description': 'Task executed'}}}}

    @decorators.catch_errors()
    @decorators.auth.required()
    def post(self):
        # celery = self.get_service_instance('celery')

        task = CeleryExt.data_task.apply_async(
            args=[], countdown=5
        )
        return self.response(task.task_id)
