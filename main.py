"""
The control script for a molecular rovibrational spectral analysis.

This script controls the user interaction with the program and
depends on a number of other scripts for the majority of the work.
A number of settings are held in a pickled configuration dictionary.
The remainder of the settings can be accessed below. Various modes
are also available for testing and visual output.

Requires: Numpy, Scipy, Matplotlib
Optional: PIL (processing file formats aside form png)

Author: Ben Yee, btyee@umich.edu
Last modified: 2012-07-11
"""

# ==============================================================================
# Advanced User settings
# TODO: replace this with an argument parser or the config file...

# Modes
debug = False
display = True

# Simulation
fwhm = 1.30e-10     # Full-width half maximum of spectral line
profile = 3         # 1: Gaussian, 2: Lorentzian, 3: Pseudo-Voigt
eta = 0.25          # Lorentzian fraction of pseudo-Voigt
temp_start = 250    # Lowest temperature to check
temp_end = 1500     # Highest temperature to check
step = 50           # Interval for temperature walk

# Dirty nasty hacks
# TODO: add a noise detection system to filter out meaningless spectra
# TODO: automate(?) time step info, maybe eliminate entirely
noise = 0.20         # Sets the noise baseline for peak
dt = 500e-12         # time step interval
shift = 0.04 * 1e-9  # simple shift of the simulated wavelength peaks

from gases import N2
istate = N2.C3Piu()
vi = 0
fstate = N2.B3Pig()
vf = 0
J = range(51)

# Don't touch stuff below this line unless you know what you're doing!
# ==============================================================================


# Standard Libraries
import sys
import Tkinter, tkFileDialog

# Third Party Libraries
import pylab
from scipy import interpolate

# Local Libraries
import config
import read
import spectrum
import temperature

print ('\n*************************************************\n'
         '* Analysis package for Rotational Spectra (0.1) *\n'
         '*************************************************\n'
         'Instructions: Choose a directory containing sequentially '
         'labeled image files. The script is recursive and searches '
         'for files of the same name. If duplicate files exist in '
         'the subdirectories, they are averaged to form a single '
         'image.\n\n'
         ''
         'You will be asked to specify the corners of a box contain'
         'ing the signal and the corners of a box containing the '
         'background. Afterward, you will be asked for the spectral '
         'size of the image (in nm) and the slit characteristics. '
         'Finally, you will be prompted for the systems and '
         'transitions you wish to simulate. This information is '
         'written to a file and can optionally be loaded for repeat '
         'analyses.\n')

if debug:
    print ' *** Debug Mode Enabled ***\n'
    pylab.ion()

# Use Tk dialog for choosing the top-level directory
root = Tkinter.Tk()
root.withdraw()
top_dir = tkFileDialog.askdirectory(parent=root, initialdir="..", 
                                    title='Pick a directory')
if top_dir is '':
    print 'No directory provided, quitting...'
    sys.exit(0)

# Recursively find parsable files, allowed file types is currently hard-
# coded in read.py. Does not check for consistency between images.
image_paths = read.find_images(top_dir)
if image_paths is None:
    'No parsable files could be found, quitting...'
    sys.exit(0)

config_path = top_dir + '/settings.pickle'
settings = config.load(config_path)
if not settings:
    print 'Generating a configuration file...\n'
    settings = config.generate(config_path, image_paths)

if debug:
    debug_index = raw_input('Type the index of the image you would like to use '
                            'for debugging purposes (0-%d):' % len(image_paths))
    debug_index = int(debug_index)


times = range(0, len(image_paths))
times = [dt * i for i in times]
ctemps = []
it = 0
test_spectra = []
minerrs = []

if debug:
    image_paths = image_paths[debug_index],

signal = pylab.array([])
for image_path in image_paths:
    print 'Image %d: ' % it,
    exp_image = None
    exp_image = spectrum.SpectrumImage(image_path, **settings)
    exp_spectrum = exp_image.collapse()
    exp_spectrum.wavelengths = exp_spectrum.wavelengths + shift
    signal = pylab.append(signal, exp_spectrum.intensities[784])
    if signal[-1] < noise:
        print 'Signal too low, setting to zero...\n'
        minerrs.append(0)
        ctemps.append(0)
        it += 1
        continue
    exp_spectrum = exp_spectrum.normalize()
    #exp_spectrum.wavelengths = 9.998381e-1 * exp_spectrum.wavelengths + 5.90766e-11

    test_temperatures = range(temp_start, temp_end+step, step)
    if not test_spectra:
        print '\n    Generating spectra (this may take a while) ...'
        for temp in test_temperatures:
            test_spectrum = temperature.lines(istate, vi, fstate, vf, J[-1], temp)
            test_spectrum = test_spectrum.map(exp_spectrum.wavelengths)
            test_spectrum = test_spectrum.broaden(fwhm, linetype=1)
            test_spectra.append(test_spectrum.normalize())

    errors = []
    for test_spectrum in test_spectra:
        errors.append(pylab.sum(abs(exp_spectrum.intensities - test_spectrum.intensities)))

    tck1 = interpolate.splrep(test_temperatures, errors, s=0)
    der1 = interpolate.splev(test_temperatures, tck1, der=1)
    tck2 = interpolate.splrep(test_temperatures, der1, s=0)
    roots = interpolate.sproot(tck2)
    if len(roots) is not 1:
        print 'Temperature ambiguous, setting to zero...'
        ctemps.append(0)
        minerrs.append(0)
    else:
        matched = temperature.lines(istate, vi, fstate, vf, J[-1], roots[-1])
        #matched.inair()
        matched = matched.map(exp_spectrum.wavelengths)
        matched = matched.broaden(fwhm, linetype=1)
        matched = matched.normalize()
        minerrs.append(sum((exp_spectrum.intensities - matched.intensities)**2))
        ctemps.append(roots)
    print '%f K\n (surface error of %f)' % (ctemps[-1], minerrs[-1])

    if debug:
        pylab.clf()
        exp_spectrum.show()
        matched.show()
        pylab.legend(['Experimental', 'Simulated'])
        print 'Error in simulation:', minerrs[-1]
        pylab.plot(exp_spectrum.wavelengths, exp_spectrum.intensities-matched.intensities)
        pylab.title('Differences')
        specfile = open('measured.csv', 'w')
        matchfile = open('simulated.csv', 'w')
        for wavelength in exp_spectrum.wavelengths:
            specfile.write('%g, %g\n' % (wavelength, exp_spectrum[wavelength]))
        for wavelength in matched.wavelengths:
            matchfile.write('%g, %g\n' % (wavelength, matched[wavelength]))
        specfile.close()
        matchfile.close()

    it += 1

if display:
    fid = open('results.csv', 'w')

    for i in range(len(ctemps)):
        fid.write('%g, %g\n' % (times[i], ctemps[i]))

    fid.close()

    pylab.plot(times, ctemps)
    signal = signal/signal.max()
    signal = signal*max(ctemps)
    pylab.plot(times, signal)
    fid = open('signal.csv', 'w')
    for i in range(len(signal)):
        fid.write('%g, %g\n' % (times[i], signal[i]))
    fid.close()
    raw_input('')
    pylab.clf()
    pylab.plot(times, minerrs,'-')

raw_input('(Analysis complete, hit return to exit)')
