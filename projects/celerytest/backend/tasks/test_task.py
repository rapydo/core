# -*- coding: utf-8 -*-

from restapi.flask_ext.flask_celery import CeleryExt

from utilities.logs import get_logger
log = get_logger(__name__)

celery_app = CeleryExt.celery_app

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"


@celery_app.task(bind=True)
def update_annotations(self):
    with celery_app.app.app_context():

        self.db = celery_app.get_service('sqlalchemy')

        log.info("Task executed!")
        return "Task executed!"
