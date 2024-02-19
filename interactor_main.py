from reason import TMS, Interactor
from z3 import *

def ex5():
    tms = TMS()
    na = tms.create_node("a")
    nb = tms.create_node("b")
    nc = tms.create_node("c")
    tms.add_constraint(None, Implies(Or(na, nb), nc))
    tms.enable_assumption(na)
    tms.enable_assumption(nb)
    tms.set_assumption(nc, False)
    return Interactor(tms).converge()

if __name__ == '__main__':
    print(ex5())
