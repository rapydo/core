# -*- coding: utf-8 -*-

from marshmallow import fields, validate
# from webargs.flaskparser import use_kwargs
from flask_apispec import use_kwargs
from flask_apispec import marshal_with
from flask_apispec import MethodResource

from restapi.models import Schema
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi import decorators
from restapi.utilities.htmlcodes import hcodes
from restapi.utilities.logs import log

# 1 - Experiments with sqlalchemy
#     https://github.com/marshmallow-code/marshmallow-sqlalchemy)
# 2 - raise errors for unknown fields? (also useful for get_schema in PUT)
# 3 - Convert some true endpoint... like admin tokens?
# 4 - convert into interfaces? https://github.com/danohu/py2ng
#     if used, please remove types from response.py and import from py2ng


class InputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=99))
    # test_date = fields.DateTime(required=True, data_key="date", format="%Y-%m-%d")
    # test_date = fields.Date(required=True, data_key="date", format="%Y-%m-%d")
    test_date = fields.Date(
        required=True,
        data_key="date",
        format='%Y-%m-%dT%H:%M:%S.000Z')
    healthy = fields.Bool(required=False, default=True)
    HGB = fields.Float(required=True, validate=validate.Range(min=0, max=30))


class Subnode(Schema):
    f = fields.Str()


class OutputSchema(InputSchema):
    uuid = fields.Str()
    # subnode = fields.List(fields.Nested(Subnode))
    subnode = fields.Nested(Subnode)

# Field that applies no formatting.
# data = fields.Raw(attribute="content")
# "Raw",
# "Nested",
# "Mapping",
# "Dict",
# "List",


class MarshalData(MethodResource, EndpointResource):

    labels = ['helpers']

    _GET = {
        "/data": {
            "summary": "Experiments with ApiSpec",
            "description": "Proof of concept for ApiSpec integration in RAPyDo",
            "responses": {"200": {"description": "Endpoint is working"}},
        }
    }
    _POST = {
        "/data": {
            "summary": "Create an entity",
            "responses": {"200": {"description": "The uuid of the entity is returned"}},
        }
    }

    _PUT = {
        "/data/<uuid>": {
            "summary": "Modify an entity",
            "responses": {"204": {"description": "Entity modified"}},
        }
    }

    _DELETE = {
        "/data/<uuid>": {
            "summary": "Delete an entity",
            "responses": {"204": {"description": "Entity deleted"}},
        }
    }

    @marshal_with(OutputSchema(many=True), code=200)
    @decorators.catch_errors()
    def get(self, **kwargs):

        graph = self.get_service_instance('neo4j')

        data = []
        for d in graph.Data.nodes.all():
            # d.subnode = d.subnode.all()

            data.append(d)

        return self.response(data)

    @use_kwargs(InputSchema)
    @decorators.catch_errors()
    def post(self, **kwargs):

        graph = self.get_service_instance('neo4j')
        d = graph.Data(**kwargs).save()

        s = graph.Subnode().save()

        d.subnode.connect(s)

        return d.uuid

    @use_kwargs(InputSchema(strip_required=True, exclude=("email",)))
    @decorators.catch_errors()
    def put(self, uuid, **kwargs):

        graph = self.get_service_instance('neo4j')

        d = graph.Data.nodes.get_or_none(uuid=uuid)

        if d is None:
            raise RestApiException("Data not found")

        for key in kwargs:
            d.__dict__[key] = kwargs[key]

        d.save()
        return self.empty_response()

    @decorators.catch_errors()
    def delete(self, uuid):

        graph = self.get_service_instance('neo4j')

        d = graph.Data.nodes.get_or_none(uuid=uuid)

        if d is None:
            raise RestApiException("Data not found")

        d.delete()

        return self.empty_response()


class TestNum(Schema):
    test_num = fields.Int(
        required=True,
        validate=validate.Range(min=1, max=3)
    )


class OutSchema(Schema):
    value = fields.Int()


class Error(Schema):
    mykey = fields.Str()


class MarshalResponses(MethodResource, EndpointResource):

    labels = ['helpers']

    _GET = {
        "/marshal": {
            "summary": "Experiments with ApiSpec",
            "description": "Proof of concept for ApiSpec integration in RAPyDo",
            "responses": {"200": {"description": "Endpoint is working"}},
        }
    }

    @use_kwargs(TestNum)
    @marshal_with(OutSchema, code=200)
    @marshal_with(Error, code=404)
    @decorators.catch_errors()
    def get(self, **kwargs):

        graph = self.get_service_instance('neo4j')

        log.debug(graph)

        test_num = kwargs.get("test_num")
        if test_num == 1:
            data = {"value": "123", "hideme": "Not returned"}
            return self.response(data)

        if test_num == 2:
            error = {"mykey": "Just an error", "hideme": "Not returned"}
            raise RestApiException(error, status_code=hcodes.HTTP_BAD_NOTFOUND)

        if test_num == 3:
            error = {"mykey": "Just an error", "hideme": "Not returned"}
            raise RestApiException(error, status_code=hcodes.HTTP_BAD_REQUEST)

        raise RestApiException("Test {} not implemented".format(test_num))


class FlatResponses(MethodResource, EndpointResource):

    labels = ['helpers']

    _GET = {
        "/flat": {
            "summary": "Experiments with ApiSpec",
            "description": "Proof of concept for ApiSpec integration in RAPyDo",
            "responses": {"200": {"description": "Endpoint is working"}},
        }
    }

    @use_kwargs(TestNum)
    @decorators.catch_errors()
    def get(self, **kwargs):

        graph = self.get_service_instance('neo4j')

        log.debug(graph)

        test_num = kwargs.get("test_num")
        if test_num == 1:
            return self.response("1")

        if test_num == 2:
            raise RestApiException("Just an error")

        raise RestApiException("Test {} not implemented".format(test_num))
