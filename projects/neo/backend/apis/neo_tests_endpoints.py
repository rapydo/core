# -*- coding: utf-8 -*-

from restapi.rest.definition import EndpointResource
from restapi.connectors.neo4j import graph_transactions

from restapi.exceptions import RestApiException
from restapi import decorators
# from restapi.utilities.logs import log


class DoTests(EndpointResource):

    labels = ['tests']
    GET = {
        '/tests/<test_num>': {
            'summary': 'Do tests',
            'responses': {'200': {'description': 'a test is executed'}}
        }
    }

    def test_1(self):
        self.graph.cypher("MATCH (n) RETURN n")

        return "1"

    def test_2(self):
        self.graph.cypher("MATCH (n) RETURN n with a syntax error")

        return "2"

    def test_3(self):
        """ Create models """

        g = self.graph.Group(name='test', extra='value')
        g.save()

        u = self.get_current_user()
        u.belongs_to.connect(g)

        t1 = self.graph.JustATest(p_str='abc', p_int=123)
        t1.save()

        rel = g.test1.connect(t1)
        rel.pp = "XYZ"
        rel.save()

        t2 = self.graph.JustATest(p_str='def', p_int=123)
        t2.save()

        rel = g.test1.connect(t2)

        return "3"

    def test_4(self):
        """ Read previously created models """

        groups = self.graph.Group.nodes.filter(name='test')
        for g in groups:
            # Just take the first
            data = {
                "name": g.name,
                "_test1": []
            }
            t = self.graph.getSingleLinkedNode(g.test1)
            data["_test1"].append(
                {
                    "p_str": t.p_str,
                }
            )
            return data

    @decorators.catch_errors()
    @graph_transactions
    @decorators.auth.required()
    def get(self, test_num):

        self.graph = self.get_service_instance('neo4j')

        if test_num == "1":
            out = self.test_1()
        elif test_num == "2":
            out = self.test_2()
        elif test_num == "3":
            out = self.test_3()
        elif test_num == "4":
            out = self.test_4()
        else:
            raise RestApiException("Test {} not found".format(test_num))

        return self.response(out)
