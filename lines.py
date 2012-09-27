import temperature
from gases import N2
from pylab import *
import operator
from scipy import interpolate

istate = N2.C3Piu()
vi = 0
fstate = N2.B3Pig()
vf = 0

Tr = 450

J = range(51)

ns = temperature.lines(istate, vi, fstate, vf, J[-1], Tr)
ns = ns.normalize()
ns.show()

#newwave = linspace(min(ns.wavelengths), max(ns.wavelengths), 10000)
#mapped = ns.map(newwave)

#smooth1 = ns.broaden()
#smooth1 = smooth1.normalize()
#smooth2 = mapped.broaden()
#smooth2 = smooth2.normalize()

#smooth1.show()
#smooth2.show()

show()

raw_input('')

fid = open('lines.csv', 'w')
output = zip(ns.wavelengths, ns.intensities)
savetxt(fid, output, delimiter=',')
fid.close()
