# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi import decorators

from flask_apispec import use_kwargs, marshal_with
from flask_apispec import MethodResource
# from flask_apispec import Ref
from marshmallow import Schema, fields, validate

from restapi.utilities.logs import log


class TestNum(Schema):
    test_num = fields.Int(required=True, validate=validate.Range(min=1, max=1))


class UserSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=4))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=40))
    created_at = fields.DateTime(required=True, format="%Y-%M-%d")


class Error(Schema):
    xyz: fields.Str()


class OutSchema(Schema):
    value = fields.Int()


class OutSchema1(Schema):
    value = fields.Str()


# Field that applies no formatting.
# data = fields.Raw(attribute="content")
# "Raw",
# "Nested",
# "Mapping",
# "Dict",
# "List",

class DoTests(MethodResource, EndpointResource):

    labels = ['helpers']

    _GET = {
        "/tests": {
            "summary": "Experiments with ApiSpec",
            "description": "Proof of concept for ApiSpec integration in RAPyDo",
            "responses": {"200": {"description": "Endpoint is working"}},
        }
    }

    @use_kwargs(TestNum)
    @marshal_with(Error, code=400)
    # @marshal_with(OutSchema, code=404)
    @marshal_with(OutSchema, code=200)
    @marshal_with(OutSchema1, code=201)
    @marshal_with(None, code=204)
    @decorators.catch_errors()
    def get(self, **kwargs):

        graph = self.get_service_instance('neo4j')

        log.debug(graph)

        if kwargs.get("test_num") == 1:
            return self.response("1")

        log.info(kwargs)

        # return self.response("blabla")
        data = {"value": "123", "xyz": "abc"}

        raise RestApiException("Just an error")
        raise RestApiException(data)
        return self.response(data)
