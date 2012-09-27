import temperature
from gases import N2
from pylab import *
import operator

istate = N2.C3Piu()
vi = 0
fstate = N2.B3Pig()
vf = 0

Tr = 450

J = range(51)

(ns, nw) = temperature.lines(istate, vi, fstate, vf, J[-1], Tr)

ns.show()

b = ['P', 'Q', 'R']
it = 0
for branch in nw:
    for num, subbranch in branch.items():
        fid = open(b[it] + str(num) + '.csv', 'w')
        output = array(sorted(subbranch.iteritems(), key=operator.itemgetter(0)))
        savetxt(fid, output, delimiter=',')
        fid.close()
    it += 1

show()
