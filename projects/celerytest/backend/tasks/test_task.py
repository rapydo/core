# -*- coding: utf-8 -*-

from restapi.flask_ext.flask_celery import CeleryExt
import time

from utilities.logs import get_logger
log = get_logger(__name__)

celery_app = CeleryExt.celery_app

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"


@celery_app.task(bind=True)
def testme(self):
    with celery_app.app.app_context():

        # self.db = celery_app.get_service('sqlalchemy')

        log.info("Task started!")

        self.update_state(state="STARTING", meta={'current': 1, 'total': 3})
        time.sleep(5)

        self.update_state(state="COMPUTING", meta={'current': 2, 'total': 3})
        time.sleep(5)

        self.update_state(state="FINAL", meta={'current': 3, 'total': 3})
        time.sleep(5)

        log.info("Task executed!")
        return "Task executed!"


# @celery_app.task(bind=True)
# def ping(self):
#     with celery_app.app.app_context():
#         return "pong"
