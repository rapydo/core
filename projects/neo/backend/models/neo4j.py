# -*- coding: utf-8 -*-

"""
Graph DB abstraction from neo4j server.
These are custom models!

VERY IMPORTANT!
Imports and models have to be defined/used AFTER normal Graphdb connection.
"""

from neomodel import ZeroOrMore, OneOrMore

from restapi.services.neo4j.models import \
    StringProperty, IntegerProperty, DateTimeProperty, \
    JSONProperty, ArrayProperty, FloatProperty, \
    IdentifiedNode, StructuredRel, TimestampedNode, \
    RelationshipTo, RelationshipFrom  # , UniqueIdProperty
from restapi.models.neo4j import User as UserBase

from utilities.logs import get_logger
log = get_logger(__name__)

__author__ = "Mattia D'Antonio (m.dantonio@cineca.it)"


# Extension of User model for accounting in API login/logout
class User(UserBase):

    belongs_to = RelationshipTo(
        'Group', 'BELONGS_TO', cardinality=ZeroOrMore, show=True)


class RelationTest(StructuredRel):
    pp = StringProperty(show=True)


class Group(IdentifiedNode):
    name = StringProperty(required=True, unique_index=True, show=True)
    members = RelationshipFrom(
        'User', 'BELONGS_TO', cardinality=ZeroOrMore, show=True)

    test = RelationshipTo(
        'JustATest', 'TEST', cardinality=OneOrMore, model=RelationTest)


class JustATest(TimestampedNode):
    p_str = StringProperty(required=True, unique_index=True, show=True)
    p_int = IntegerProperty()
    p_arr = ArrayProperty()
    p_json = JSONProperty()
    p_float = FloatProperty()
    p_dt = DateTimeProperty()

    test = RelationshipFrom(
        'Group', 'TEST', cardinality=ZeroOrMore, model=RelationTest)
