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

        # TESTING HOME
        home = irods.get_user_home()

        assert irods.get_user_home("xxyyzz") == "/tempZone/home/xxyyzz"
        assert home == "/tempZone/home/irods"

        path = irods.get_absolute_path("tempZone", "home", "irods")
        assert path == home

        # DEFINING SOME PATHS
        data_obj = os.path.join(path, "test.txt")
        collection = os.path.join(path, "sub")
        # collection2 = os.path.join(path, "sub2")
        data_obj2 = os.path.join(collection, "test2.txt")
        data_obj3 = os.path.join(collection, "test3.txt")

        # BASIC TESTS ON EXISTANCE
        assert irods.get_collection_from_path(data_obj) == path

        assert irods.exists(path)
        assert not irods.exists(data_obj)

        assert irods.is_collection(path)
        assert not irods.is_collection(data_obj)

        assert not irods.is_dataobject(path)
        assert not irods.is_dataobject(data_obj)

        # CREATE FIRST COLLECTIONN AND FIRST FILE
        irods.create_empty(collection, directory=True)
        irods.create_empty(data_obj)

        assert irods.exists(collection)
        assert irods.exists(data_obj)

        assert irods.is_collection(collection)
        assert not irods.is_collection(data_obj)

        assert not irods.is_dataobject(collection)
        assert irods.is_dataobject(data_obj)

        content = irods.list(path)
        # here we should find only collection and data_obj
        assert len(content) == 2
        assert "sub" in content
        assert "test.txt" in content

        # COPY AND MOVE
        irods.copy(data_obj, data_obj2)
        irods.move(data_obj2, data_obj3)
        # irods.copy(collection, collection2, recursive=True)

        content = irods.list(path)
        # here we should also find data_obj3
        assert len(content) == 3
        assert "sub" in content
        assert "test.txt" in content
        assert "test3.txt" in content

        irods.remove(data_obj3)
        content = irods.list(path)
        # here we should no longer find data_obj3
        assert len(content) == 2
        assert "sub" in content
        assert "test.txt" in content
        assert "test3.txt" not in content

        # irods.remove(collection2, recursive=True)
        # content = irods.list(path)
        # here we should also find collection2
        # assert content == {}
