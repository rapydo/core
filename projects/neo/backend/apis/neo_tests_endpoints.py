# -*- coding: utf-8 -*-

# from flask import current_app
# from restapi.rest.definition import EndpointResource
from restapi.services.neo4j.graph_endpoints import GraphBaseOperations
from restapi.services.neo4j.graph_endpoints import graph_transactions
from restapi.exceptions import RestApiException
from restapi.decorators import catch_error
from restapi.protocols.bearer import authentication
from restapi.utilities.meta import Meta
from restapi.utilities.logs import get_logger

log = get_logger(__name__)


# if current_app.config['TESTING']:
class DoTests(GraphBaseOperations):

    # schema_expose = True
    labels = ['tests']
    GET = {'/tests/<test_num>': {'custom': {}, 'summary': 'Do tests', 'responses': {'200': {'description': 'a test is executed'}}}}

    def test_1(self, graph):
        graph.cypher("MATCH (n) RETURN n")

        return "1"

    def test_2(self, graph):
        graph.cypher("MATCH (n) RETURN n with a syntax error")

        return "2"

    def test_3(self, graph):
        """ Create models """

        g = graph.Group(name='test', extra='hidden')
        g.save()

        u = self.get_current_user()
        u.belongs_to.connect(g)

        t1 = graph.JustATest(p_str='abc', p_int=123)
        t1.save()

        rel = g.test1.connect(t1)
        rel.pp = "XYZ"
        rel.save()

        t2 = graph.JustATest(p_str='def', p_int=123)
        t2.save()

        rel = g.test1.connect(t2)

        return "3"

    def test_4(self, graph):
        """ Read previously created models """

        groups = graph.Group.nodes.filter(name='test')
        for g in groups:
            # Just take the first
            j = self.getJsonResponse(g)
            # log.exit(j)
            return j

    @catch_error()
    @graph_transactions
    @authentication.required()
    def get(self, test_num):

        self.graph = self.get_service_instance('neo4j')

        meta = Meta()
        methods = meta.get_methods_inside_instance(self)
        method_name = "test_%s" % test_num
        if method_name not in methods:
            raise RestApiException("Test %d not found" % test_num)
        method = methods[method_name]
        out = method(self.graph)
        return self.force_response(out)
