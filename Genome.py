from Node import Node
import random
from math import exp


class Genome:

    def __init__(self):

        self.connections = []
        self.bias = Node(0, 0)
        self.inp = [self.bias]
        self.out = []
        self.connection_set = set()  # it is used to check if a connection between two nodes already exists in a genome
        self.fitness = 0
        self.nodes = [self.bias]

    #  Returns a list of output given a input list
    def output(self, input_v):

        for n in self.nodes:
            n.value = 0
        self.bias.value = 1
        self.inp.sort(key=lambda x: x.id_n)
        self.out.sort(key=lambda x: x.id_n)
        for i, n in zip(input_v, self.inp[1:]):
            n.value = i
        for _ in range(7):
            random.shuffle(self.nodes)
            for n in self.nodes:
                if n.layer == 2:
                    s = 0
                    for c in n.in_con:

                        if c.enabled:
                            s += c.inp.value * c.weight
                    n.value = self.m_sigmoid(s)
        for n in self.out:
            s = 0
            for c in n.in_con:
                if c.enabled:
                    s += c.inp.value * c.weight
            n.value = self.m_sigmoid(s)
        r = []
        for o in self.out:
            r.append(o.value)
        return r

    # activation function
    # Staticmethod is written because it does not use any variables or methods/functions of the class
    @staticmethod
    def m_sigmoid(x):
        return 1/(1 + exp(-4.9*x)) if x > -15 else 0

    # adds new inherited connection to the genome
    def add_connection(self, connect_gene):

        if connect_gene.innov_no in self.gen_innov():
            for c in self.connections:
                if c.innov_no == connect_gene.innov_no:
                    c.weight = connect_gene.weight
                    c.enabled = connect_gene.enabled
                    return

        iid, oid = connect_gene.inp.id_n, connect_gene.out.id_n

        if (iid, oid) in self.connection_set or (oid, iid) in self.connection_set:
            return
        connect_gene.inp.in_con = []
        connect_gene.out.in_con = []

        if iid in self.node_ids():
            for n in self.nodes:
                if n.id_n == iid:
                    connect_gene.inp = n
                    break

        else:
            self.nodes.append(connect_gene.inp)

        if oid in self.node_ids():
            for n in self.nodes:
                if n.id_n == oid:
                    n.in_con.append(connect_gene)
                    connect_gene.out = n
                    break
        else:
            connect_gene.out.in_con.append(connect_gene)
            self.nodes.append(connect_gene.out)

        self.connections.append(connect_gene)
        self.connection_set.add((connect_gene.inp.id_n, connect_gene.out.id_n))

    # returns the set of innovation number in the connection genes
    def gen_innov(self):
        s = set()
        for c in self.connections:
            s.add(c.innov_no)
        return s

    # returns the set of id number of all nodes
    def node_ids(self):
        s = set()
        for n in self.nodes:
            s.add(n.id_n)
        return s
