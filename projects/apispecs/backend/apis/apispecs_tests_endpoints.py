# -*- coding: utf-8 -*-

from marshmallow import fields, validate
# from webargs.flaskparser import use_kwargs
from flask_apispec import use_kwargs
from flask_apispec import marshal_with
from flask_apispec import MethodResource
from flask_apispec.annotations import doc

from restapi.models import Schema
from restapi.services.detect import detector
from restapi.rest.definition import EndpointResource
from restapi.exceptions import RestApiException
from restapi import decorators
# from restapi.utilities.logs import log

from apispecs.models.neo4j import BLOOD_TYPES

# 1 - Experiments with sqlalchemy
#     https://github.com/marshmallow-code/marshmallow-sqlalchemy)
# 2 - raise errors for unknown fields? (also useful for get_schema in PUT)


def get_referall_names():
    neo4j = detector.get_service_instance('neo4j')
    return [n.name for n in neo4j.Data.nodes.all()]


class InputSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    age = fields.Int(required=True, validate=validate.Range(min=18, max=99))
    # test_date = fields.DateTime(required=True, data_key="date", format="%Y-%m-%d")
    # test_date = fields.Date(required=True, data_key="date", format="%Y-%m-%d")
    test_date = fields.Date(
        required=True,
        data_key="date",
        format='%Y-%m-%dT%H:%M:%S.000Z')
    healthy = fields.Bool(required=False, default=True)
    blood_type = fields.Str(
        required=True,
        validate=validate.OneOf(
            choices=[element[0] for element in BLOOD_TYPES],
            labels=[element[1] for element in BLOOD_TYPES]
        )
    )
    # OneOf
    HGB = fields.Float(required=True, validate=validate.Range(min=0, max=30))
    referral = fields.Str(
        required=False,
        validate=validate.OneOf(
            choices=get_referall_names()
        )
    )


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

    @doc(responses={"200": {"description": "Endpoint is working"}})
    @doc(
        summary="Experiments with ApiSpec",
        description="Proof of concept for ApiSpec integration in RAPyDo"
    )
    @marshal_with(OutputSchema(many=True), code=200)
    @decorators.catch_errors()
    @decorators.auth.required()
    def get(self, **kwargs):

        graph = self.get_service_instance('neo4j')

        data = []
        for d in graph.Data.nodes.all():
            # d.subnode = d.subnode.all()

            data.append(d)

        return self.response(data)

    @decorators.catch_errors()
    @decorators.auth.required()
    @use_kwargs(InputSchema())
    def post(self, **kwargs):

        graph = self.get_service_instance('neo4j')
        d = graph.Data(**kwargs).save()

        s = graph.Subnode().save()

        d.subnode.connect(s)

        return d.uuid

    @decorators.catch_errors()
    @decorators.auth.required()
    @use_kwargs(InputSchema(strip_required=True, exclude=("email",)))
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
    @decorators.auth.required()
    def delete(self, uuid):

        graph = self.get_service_instance('neo4j')

        d = graph.Data.nodes.get_or_none(uuid=uuid)

        if d is None:
            raise RestApiException("Data not found")

        d.delete()

        return self.empty_response()
