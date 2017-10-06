# -*- coding: utf-8 -*-

# from flask import current_app
# from restapi.rest.definition import EndpointResource
from restapi.services.neo4j.graph_endpoints import GraphBaseOperations
from restapi.services.neo4j.graph_endpoints import graph_transactions
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from utilities.meta import Meta
from utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(GraphBaseOperations):

    def test_1(self, graph):
        graph.cypher("MATCH (n) RETURN n")

        return "1"

    def test_2(self, graph):
        graph.cypher("MATCH (n) RETURN n with a syntax error")

        return "2"

    def test_3(self, graph):
        """ Create models """

        g = graph.Group(name='test')
        g.save()

        u = self._current_user
        u.belongs_to.connect(g)

        t = graph.JustATest(p_str='abc', p_int=123)

        rel = g.test.connect(t)
        rel.pp = "XYZ"
        rel.save()

        return "3"

    def test_4(self, graph):
        """ Read previously created models """

        g = graph.Group(name='test')
        return self.getJsonResponse(g)

    @catch_error()
    @graph_transactions
    def get(self, test_num):

        # self.graph = self.get_service_instance('neo4j')
        self.initGraph()

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_%s" % test_num
        if method_name not in methods:
            raise RestApiException("Test %d not found" % test_num)
        method = methods[method_name]
        out = method(self.graph)
        return self.force_response(out)
