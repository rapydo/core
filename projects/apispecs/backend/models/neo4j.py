# -*- coding: utf-8 -*-

"""
Graph DB abstraction from neo4j server.
These are custom models!

VERY IMPORTANT!
Imports and models have to be defined/used AFTER normal Graphdb connection.
"""

from neomodel import ZeroOrMore, OneOrMore

from neomodel.util import NodeClassRegistry

from restapi.connectors.neo4j.types import (
    StringProperty,
    IntegerProperty,
    DateProperty,
    DateTimeProperty,
    JSONProperty,
    ArrayProperty,
    FloatProperty,
    BooleanProperty,
    AliasProperty,
    IdentifiedNode,
    StructuredRel,
    TimestampedNode,
    RelationshipTo,
    RelationshipFrom,
    # UniqueIdProperty
)

# from restapi.utilities.logs import log


class Data(TimestampedNode):
    name = StringProperty(required=True)
    email = StringProperty(required=True)
    age = IntegerProperty(required=True)
    # test_date = DateTimeProperty(required=True)
    test_date = DateProperty(required=True)
    healthy = BooleanProperty(required=False, default=True)
    HGB = FloatProperty(required=True)
