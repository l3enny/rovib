import csv
from numpy import array, append, exp
from pylab import *

target = 'signal.csv'

signals = array([])
times = array([])

fid = open(target, 'r')
data = csv.reader(fid)
for row in data:
    times = append(times, float(row[0]))
    signals = append(signals, float(row[1]))

def fit(t):
    A = 100e6 # Random guess
    t0 = 16.0e-9 # Time when curve appears to begin exponentional fall
    peak = 892.828 # Intensity when curve appears to begin exponential fall
    return peak * exp(-A * (t-t0))
def pancheshnyi(t):
    A = 64.446e6 # Calculated per Pancheshnyi (1998) values
    t0 = 15.52e-9 -3e-9 # Adjust for best fit
    peak = 973.508 # Peak recorded intensity
    return peak * exp(-A * (t-t0))

ion()
plot(times, signals, '.-k')
plot(times, fit(times), '-r')
plot(times, pancheshnyi(times), '-g')
axis([0.0, 55e-9, 0.0, 1e3])
xlabel('Time Delay (ns)')
ylabel('337.1 nm Intensity (a.u.)')
legend(['Measured', 'Guess, $\tau$ = 10 ns', 'Pancheshnyi, $\tau$ = 15.517 ns'])
raw_input('')
