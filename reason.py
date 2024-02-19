from z3 import *

from dataclasses import dataclass

@dataclass
class SAT:
    model: object

@dataclass
class UNSAT:
    core: object

Result = SAT | UNSAT

UNKNOWN = None
TRUE = True
FALSE = False

class Node:
    def __init__(self, var, index, datum, assumptionp, tms, label = UNKNOWN):
        self.var = var
        self.index = index
        self.datum = datum
        self.assumptionp = assumptionp
        self.tms = tms
        self.label = label

class Constraint:
    def __init__(self, index, informant, relation):
        self.index = index
        self.informant = informant
        self.relation = relation

class TMS:
    def __init__(self):
        self.node_counter = 0
        self.nodes_by_datum = {}
        self.nodes_by_var = {}
        self.constraint_counter = 0
        self.constraints = []
    def add_constraint(self, informant, relation):
        self.constraint_counter += 1
        c = Constraint(self.constraint_counter, informant, relation)
        self.constraints += [c]
        return c
    def create_node(self, datum, assumptionp = True):
        assert datum not in self.nodes_by_datum
        self.node_counter += 1
        variable = Bool(datum)
        node = Node(variable, self.node_counter, datum, assumptionp, self)
        self.nodes_by_datum[datum] = node
        self.nodes_by_var[variable] = node
        return variable
    def set_assumption(self, variable, label):
        node = self.nodes_by_var[variable]
        assert node.assumptionp
        node.label = label


    def justify_node(self, informant, conclusion, premises):
        return self.add_constraint(
            informant,
            Implies(And(*premises), conclusion))
    def enable_assumption(self, variable):
        self.set_assumption(variable, TRUE)

class TMSSolver:
    def __init__(self, tms):
        self.tms = tms

    def sat(self):
        self.solver = Solver()
        self.solver.set(unsat_core=True)
        self.add_constraints()
        c = self.solver.check()
        if c == sat:
            return SAT(self.model())
        elif c == unsat:
            return UNSAT(self.solver.unsat_core())
        else:
            assert c == unknown
            return None

    def model(self):
        return self.solver.model()

    def add_constraints(self):
        for (x,node) in self.tms.nodes_by_var.items():
            if node.label != UNKNOWN:
                if node.label == TRUE:
                    self.solver.assert_and_track(x, x)
                else:
                    notx = Bool(f"Not({node.datum})")
                    self.solver.add(Xor(notx, x))
                    self.solver.assert_and_track(Not(x), notx)
        for constraint in self.tms.constraints:
            self.solver.add(constraint.relation)

class Interactor:
    def __init__(self, tms):
        self.tms = tms

    def converge(self):
        while True:
            match TMSSolver(self.tms).sat():
                case SAT(model):
                    return model
                case UNSAT(core):
                    print(core)
                    inp = input("Which to retract? ")
                    datum = inp
                    label = True
                    if inp.startswith("Not(") and inp.endswith(")"):
                        datum = inp[len("Not("):-1]
                        label = False
                    node = self.tms.nodes_by_datum[datum]
                    self.tms.set_assumption(node.var, not label)
