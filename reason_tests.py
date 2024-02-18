from reason import TMS, TMSSolver
from z3 import *

def ex1():
    tms = TMS()
    na = tms.create_node("a")
    nb = tms.create_node("b")
    nc = tms.create_node("c")
    nd = tms.create_node("d")
    ne = tms.create_node("e")
    nf = tms.create_node("f")
    ng = tms.create_node("g")
    tms.justify_node("j1", nf, [na, nb])
    tms.justify_node("j2", ne, [nb, nc])
    tms.justify_node("j3", ng, [na, ne])
    tms.justify_node("j4", ng, [nd, ne])
    tms.enable_assumption(na)
    tms.enable_assumption(nb)
    tms.enable_assumption(nc)
    tms.enable_assumption(nd)
    return TMSSolver(tms).sat()

def ex2():
    tms = TMS()
    nx = tms.create_node("x")
    ny = tms.create_node("y")
    nz = tms.create_node("z")
    nr = tms.create_node("r")
    tms.add_constraint(None, Or(nx, ny))
    tms.add_constraint(None, Or(Not(ny), nz))
    tms.add_constraint(None, Or(Not(nz), nr))
    tms.set_assumption(nx, False)
    return TMSSolver(tms).sat()
    
if __name__ == '__main__':
    print(ex1())
    print(ex2())

