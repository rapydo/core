# -*- coding: utf-8 -*-

"""
Graph DB abstraction from neo4j server.
These are custom models!

VERY IMPORTANT!
Imports and models have to be defined/used AFTER normal Graphdb connection.
"""

from neomodel import ZeroOrMore

from restapi.connectors.neo4j.types import (
    StringProperty,
    IntegerProperty,
    DateProperty,
    # DateTimeProperty,
    FloatProperty,
    BooleanProperty,
    TimestampedNode,
    RelationshipTo,
    RelationshipFrom,
)

# from restapi.utilities.logs import log

BLOOD_TYPES = (
    ("0+", "0+"),
    ("A+", "A+"),
    ("B+", "B+"),
    ("AB+", "AB+"),
    ("0-", "0-"),
    ("A-", "A-"),
    ("B-", "B-"),
    ("AB-", "AB-"),
)


class Data(TimestampedNode):
    name = StringProperty(required=True)
    email = StringProperty(required=True)
    age = IntegerProperty(required=True)
    # test_date = DateTimeProperty(required=True)
    test_date = DateProperty(required=True)
    healthy = BooleanProperty(required=False, default=True)
    blood_type = StringProperty(required=True, choices=BLOOD_TYPES)
    HGB = FloatProperty(required=True)

    subnode = RelationshipTo('Subnode', 'HAS_SUBNODE', cardinality=ZeroOrMore)


class Subnode(TimestampedNode):
    f = StringProperty(default='default value')

    data = RelationshipFrom('Data', 'HAS_SUBNODE', cardinality=ZeroOrMore)
