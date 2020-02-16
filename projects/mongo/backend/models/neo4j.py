# -*- coding: utf-8 -*-

"""
Graph DB abstraction from neo4j server.
These are custom models!

VERY IMPORTANT!
Imports and models have to be defined/used AFTER normal Graphdb connection.
"""

import logging
from neomodel import StringProperty, StructuredNode

log = logging.getLogger(__name__)


class Person(StructuredNode):
    name = StringProperty(unique_index=True)
