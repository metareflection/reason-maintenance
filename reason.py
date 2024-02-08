from z3 import *

UNKNOWN = None
TRUE = True
FALSE = False

class Node:
    def __init__(self, index, datum, assumptionp, tms, label = UNKNOWN):
        self.index = index
        self.datum = datum
        self.assumptionp = assumptionp
        self.tms = tms
        self.label = label

class Constraint:
    def __init__(self, index, informant, relation, nodes):
        self.index = index
        self.informant = informant
        self.relation = relation
        self.nodes = nodes

class TMS:
    def __init__(self):
        self.node_counter = 0
        self.nodes = {}
        self.constraint_counter = 0
        self.constraints = []
    def add_constraint(self, informant, relation, nodes):
        self.constraint_counter += 1
        c = Constraint(self.constraint_counter, informant, relation, nodes)
        self.constraints += [c]
        return c
    def create_node(self, datum, assumptionp = True):
        assert datum not in self.nodes
        self.node_counter += 1
        node = Node(self.node_counter, datum, assumptionp, self)
        self.nodes[datum] = node
        return node
    def set_assumption(self, node, label):
        assert node.assumptionp
        node.label = label


    def justify_node(self, informant, conclusion, premises):
        return self.add_constraint(
            informant,
            lambda xs: Implies(And(*xs[1:]), xs[0]),
            [conclusion] + premises)
    def enable_assumption(self, node):
        self.set_assumption(node, TRUE)

class TMSSolver:
    def __init__(self, tms):
        self.tms = tms

    def sat(self):
        self.solver = Solver()
        self.variables = self.create_variables()
        self.add_constraints()
        if self.solver.check() == sat:
            return self.model()
        else:
            return None

    def model(self):
        return self.solver.model()

    def create_variables(self):
        return dict([(node.datum, Bool(node.datum)) for node in self.tms.nodes.values()])

    def to_vars(self, nodes):
        return [self.variables[node.datum] for node in nodes]

    def add_constraints(self):
        for (datum,x) in self.variables.items():
            node = self.tms.nodes[datum]
            if node.label != UNKNOWN:
                self.solver.add(x if node.label == TRUE else Not(x))
        for constraint in self.tms.constraints:
            self.solver.add(constraint.relation(self.to_vars(constraint.nodes)))
