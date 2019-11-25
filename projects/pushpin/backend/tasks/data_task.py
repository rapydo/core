# -*- coding: utf-8 -*-

from restapi.flask_ext.flask_celery import CeleryExt
import time

from restapi.utilities.logs import get_logger
log = get_logger(__name__)

celery_app = CeleryExt.celery_app


@celery_app.task(bind=True)
def data_task(self):
    with celery_app.app.app_context():

        socket = celery_app.get_service('pushpin')

        log.info("Task started!")

        socket.publish_on_socket(self.request.id, "Task Started", sync=False)
        self.update_state(state="STARTING", meta={'current': 1, 'total': 3})
        time.sleep(5)

        socket.publish_on_socket(self.request.id, "Task is Running", sync=False)
        self.update_state(state="COMPUTING", meta={'current': 2, 'total': 3})
        time.sleep(5)

        socket.publish_on_socket(self.request.id, "Task Completed!", sync=False)
        self.update_state(state="FINAL", meta={'current': 3, 'total': 3})
        time.sleep(5)

        log.info("Task executed!")
        return "Task executed!"
