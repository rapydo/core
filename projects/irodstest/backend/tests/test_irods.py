# -*- coding: utf-8 -*-

import os
from restapi.tests import BaseTests
from restapi.tests.utilities import API_URI
from restapi.services.detect import detector
from utilities.htmlcodes import HTTP_OK_BASIC
from utilities.logs import get_logger

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"
log = get_logger(__name__)


class TestApp(BaseTests):

    def test_01_x(self, client):

        endpoint = API_URI + '/tests/1'
        r = client.get(endpoint)
        assert r.status_code == HTTP_OK_BASIC

        irods_ext = detector.extensions_instances.get('irods')
        irods = irods_ext.get_instance()

        home = irods.get_user_home()

        assert home == "/tempZone/home/irods"

        path = irods.get_absolute_path("tempZone", "home", "irods")
        assert path == home

        data_obj = os.path.join(path, "test.txt")
        collection = os.path.join(path, "sub")
        collection2 = os.path.join(path, "sub2")
        data_obj2 = os.path.join(collection, "test2.txt")
        data_obj3 = os.path.join(collection, "test3.txt")

        collection = irods.get_collection_from_path(data_obj)
        assert collection == path

        assert irods.exists(path)
        assert not irods.exists(data_obj)

        assert irods.is_collection(path)
        assert not irods.is_collection(data_obj)

        assert not irods.is_dataobject(path)
        assert not irods.is_dataobject(data_obj)

        sub_path = irods.getPath(path, "/tempZone")
        assert sub_path == "home/irods"

        irods.create_empty(collection, directory=True)
        irods.create_empty(data_obj)

        assert irods.exists(collection)
        assert irods.exists(data_obj)

        assert irods.is_collection(collection)
        assert not irods.is_collection(data_obj)

        assert not irods.is_dataobject(collection)
        assert irods.is_dataobject(data_obj)

        irods.copy(data_obj, data_obj2)
        irods.move(data_obj2, data_obj3)
        irods.copy(collection, collection2, recursive=True)

        content = irods.list(path)
        assert content == {}

        irods.remove(data_obj3)
        content = irods.list(path)
        assert content == {}

        irods.remove(collection2, recursive=True)
        content = irods.list(path)
        assert content == {}
