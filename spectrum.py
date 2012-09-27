""" Defines two classes for spectra. The first is a simple container for
an arbitrary number of sets containing wavelength and intensity data. It
also features a number of helper functions for displaying, adding and
subtracting spectra. The second class is a container for a 2D image of a
spectrum, it also features several functions for interactively selecting
background and data regions.
"""

import sys
import pylab
from pylab import exp, pi, log
from scipy import special

class Spectrum(object):
    """ A spectrum object containing wavelengths and associated
    intensities. Operator overloading is used to provide simple
    support for various spectral manipulations (convolutions,
    background subtraction, etc.).
    """

    def __init__(self, wavelengths=[], intensities=[]):
        """ spec = Spectrum([wavelengths[, intensities]]),initializes
        spectrum in a dict-like object.

        Data may be specified upon initialization. A 1D array, list, tuple
        or similarly indexed data container may be used. If the wavelengths
        are specified without intensities then all the intensities are
        initialized to zero.
        """
        wavelengths = [float(i) for i in wavelengths]
        intensities = [float(i) for i in intensities]
        if len(wavelengths) and not len(intensities):
            self.wavelengths = pylab.array(wavelengths)
            self.intensities = pylab.array([0.0] * len(wavelengths))
        elif not len(wavelengths) and len(intensities):
            raise ValueError('The wavelengths for the spectrum must be '
                             'specified.')
        elif len(wavelengths) != len(intensities):
            raise ValueError('The wavelengths and intensities must have the '
                             'same number of items')
        else:
            self.wavelengths = pylab.array(wavelengths)
            self.intensities = pylab.array(intensities)

    def __add__(self, other):
        """ spec1 + spec2 -> spec3, adds spectrum objects together
        
        Returns a new Spectrum object composed of data from two
        input spectra. For matching wavelengths, the intensities
        are added, otherwise the data from the two spectra are
        simply merged.
        """
        output = Spectrum(self.wavelengths, self.intensities)
        for wavelength, intensity in other:
            if output[wavelength]:
                output[wavelength] += intensity
            else:
                output[wavelength] = intensity
        return output

    def __iter__(self):
        for wavelength, intensity in zip(self.wavelengths, self.intensities):
            yield wavelength, intensity

    def __getitem__(self, wavelength):
        index, = pylab.where(self.wavelengths == wavelength)
        if pylab.any(index.shape):
            return self.intensities[index]
        else:
            return None

    def __setitem__(self, wavelength, intensity):
        index, = pylab.where(self.wavelengths == wavelength)
        if pylab.any(index.shape):
            self.intensities[index] = intensity
        else:
            index, = pylab.where(self.wavelengths < wavelength)
            if pylab.any(index.shape):
                self.wavelengths = pylab.insert(self.wavelengths, index[-1] + 1,
                                                wavelength)
                self.intensities = pylab.insert(self.intensities, index[-1] + 1,
                                                intensity)
            else:
                self.wavelengths = pylab.insert(self.wavelengths, 0, wavelength)
                self.intensities = pylab.insert(self.intensities, 0, intensity)

    def __sub__(self, other):
        """ spec1 - spec2 -> spec3, subtracts Spectrum objects

        Generates a new Spectrum object from two specified spectra.
        Method checks for duplicate wavelengths and properly subtracts
        the second spectrum from the first. Returns the new Spectrum object
        """
        output = Spectrum(self.wavelengths, self.intensities)
        for wavelength, intensity in other:
            if output[wavelength]:
                output[wavelength] -= intensity
            else:
                output[wavelength] = -intensity
        return output
    
    def show(self):
        """Spectrum.show(), plots the Spectrum using matplotlib methods

        The Spectrum is plotted using the line plot method from matplotlib
        with the wavelengths as the x values and the intensities as the y
        values. 
        """
        lines, = pylab.plot(self.wavelengths, self.intensities)
        return lines

    def normalize(self, ref=1):
        """ Spectrum.normalize([ref=1]), normalizes intensities to ref

        Finds the maximum intensity for the Spectrum object and then uses
        that value to normalize all intensities to ref. Modifies the object,
        and simply returns the value used for normalizing the spectra.
        """
        maximum = max(abs(self.intensities))
        return Spectrum(self.wavelengths, ref * self.intensities/maximum)
    
    def map(self, wavelengths):
        output = Spectrum(wavelengths)
        for wavelength, intensity in self:
            index, = pylab.where(output.wavelengths < wavelength)
            try:
                index = index[-1]
            except IndexError:
                output.intensities[0] += intensity
            if index == len(output.wavelengths) + 1:
                output.intensities[-1] += intensity
            elif index:
                width = output.wavelengths[index + 1] - output.wavelengths[index]
                temp = intensity * (output.wavelengths[index + 1] \
                       - wavelength) / width
                output.intensities[index] += temp
                output.intensities[index + 1] += intensity - temp
        return output
            
    def broaden(self, fwhm=1e-10, linetype=1, eta=[]):
        output = Spectrum(self.wavelengths)
        window = max(output.wavelengths) - min(output.wavelengths)
        center = max(output.wavelengths) - window/2

        if fwhm <= 0:
            raise ValueError('The linewidth must be positive and nonzero.')

        # Trapezoidal 
        elif linetype is 0:
            pass

        # Gaussian
        elif linetype is 1:
            sigma = fwhm / (2 * log(2)**0.5)
            slit = exp(-(output.wavelengths - center)**2/(2 * sigma**2))

        # Lorentzian
        elif linetype is 2:
            gamma = fwhm
            slit = 0.5 * (gamma / ((output.wavelengths - center)**2 \
                                    + 0.25 * gamma**2)) / pi

        # Pseudo-Voigt
        elif linetype is 3:
            if not eta:
                print "Eta required for pseudo-Voigt profile, quitting"
                sys.exit(0)
            sigma = fwhm
            sigma_g = fwhm / (2 * log(2)**0.5)
            g = exp(-(output.wavelengths - center)**2/(2 * sigma_g**2)) \
                / (sigma_g * (2*pi)**0.5)
            l = (0.5 * sigma / pi) \
                / ((output.wavelengths - center)**2 + .25 * sigma**2)
            slit = eta * l + (1 - eta) * g


        output.intensities = pylab.convolve(self.intensities, slit, 'same')

        return output

    def inair(self):
        def v2a(w):
            w = w/1e-10
            w = w/(1.0 + 2.735182e-4 + 131.4182/w**2 + 2.76249e8/w**4)
            return 1e-10 * w
        self.wavelengths = [v2a(w) for w in self.wavelengths]

class SpectrumImage(object):
    """A 2D image of a spectrum (likely a slit image from a CCD). Provides
    methods for defining and drawing regions as background or data, 
    displaying the image, and for collapsing the image to a Spectrum
    object.
    """
    def __init__(self, path, waveaxis=None, regions=None, start=None, end=None):
        """ SpectrumImage(path[, waveaxis[, regions]]) initializes a new
        spectrum image from the specified image path.

        Upon initialization, the image is read in to a numpy ndarray, this
        method currently assumes that 2 of the three color channels are
        redundant and eliminates them. At the time of initialization, the
        wavelength axis (0 - columns, 1 - rows) may be specified as well
        as a tuple of lists representing regions in the form [min, max].
        """
        self.image = pylab.imread(path)
        self.image = self.image[:,:,0]
        self.start = start
        self.end = end
        self.regions = []
        if waveaxis is 0 or waveaxis is 1:
            self.waveaxis = waveaxis
            for region in regions:
                bounds = self._validateregion([region['min'], region['max']])
                try:
                    self.regions.append({'min': bounds[0], 'max': bounds[1],
                                         'group': region['group']})
                except TypeError:
                    pass
        elif waveaxis is not None:
            raise ValueError('If the wavelength axis is specified it must',  
                             'be 0 or 1.')
                
    def selectregion(self, group=None):
        """ SpectrumImage.selectregion([group]), adds a region to the
        specified group from mouse input.

        Uses matplotlib's graphical input function to select two bounds
        for a region. Passes these to the validation function and then
        appends them to the region list.
        """
        points = pylab.ginput(n=2, timeout=0)
        bounds = [int(point[not self.waveaxis]) for point in points]
        bounds = self._validateregion(bounds)
        try:
            self.regions.append({'min': bounds[0], 'max': bounds[1],
                                 'group': group})
        except TypeError:
            pass

    def _validateregion(self, bounds):
        """ Accepts two points in list format, sorts them and compares
        their values to existing region boundaries. If they conflict
        with these boundaries, the values are automatically adjusted
        for validity or the method returns None for redundant boundaries.
        """
        bounds.sort()
        for region in self.regions:
            if region['min'] <= bounds[0] and region['max'] >= bounds[1]:
                return None
            elif region['min'] >= bounds[0] and region['max'] <= bounds[1]:
                i = self.regions.index(region)
                del self.regions[i]
                self.regions.append({'min': bounds[0], 'max': bounds[1], 
                                     'group': group})
            elif region['min'] <= bounds[0] <= region['max'] and \
                    region['max'] < bounds[1]:
                bounds[0] = region['max'] + 1
            elif region['min'] <= bounds[1] <= region['max'] and \
                    region['min'] > bounds[0]:
                bounds[1] = region['min'] - 1
        return bounds

    def drawregions(self, group=None, fc='red', ec='black'):
        """ SpectrumImage.drawregions([group][, fc][, ec]) draws
        regions over existing image.

        Draws a solid rectangle representing each region with a select
        group with a face color of fc and an edge color of ec.
        """
        if group:
            chosen = [region for region in self.regions \
                      if region['group'] is group]
        else:
            chosen = self.regions
        axes = pylab.gca()
        for region in chosen:
            if not self.waveaxis:
                x1, x2 = axes.get_xlim()
                y1, y2 = region['min'], region['max']
            else:
                x1, x2 = region['min'], region['max']
                y1, y2 = axes.get_ylim()
            rect = pylab.Rectangle((x1, y1), x2 - x1, y2 - y1, facecolor=fc,
                                   edgecolor=ec)
            axes.add_patch(rect)
        pylab.draw()

    def show(self):
        """ SpectrumImage.show(), draws the SpectrumImage to a set of axes.

        Uses matplotlib's imshow() function to draw the image. This method
        defaults to a heat map for grayscale images.
        """
        axesimage = pylab.imshow(self.image)
        return axesimage

    def collapse(self):
        """ SpectrumImage.collapse(), collapses a spectrum image to
        a spectrum.

        Takes a spectrum image, averages the background regions and 
        subtracts them from the data regions. The output is a single
        spectrum as the method assumes all data regions represent the
        same data. The wavelength list is generated from a given start
        and end value (assumed to be in nm). Returns the data spectrum.
        """
        try:
            wavelengths = pylab.linspace(self.start, self.end,
                                         self.image.shape[not self.waveaxis])
        except TypeError:
            print 'The starting and ending wavelengths must be specified.'
        background = pylab.zeros(len(wavelengths))
        backgroundlines = 0
        data = pylab.zeros(len(wavelengths))
        datalines = 0
        for region in self.regions:
            if region['group'] is 0:
                backgroundlines += region['max'] - region['min']
                background += self.image[region['min']:region['max'] + 1, :]\
                                  .sum(axis=self.waveaxis)
            else:
                datalines += region['max'] - region['min']
                data += self.image[region['min']:region['max'] + 1, :]\
                            .sum(axis=self.waveaxis)
        background = [sum/backgroundlines for sum in background]
        data = [sum/datalines for sum in data]
        corrected = pylab.array(data) - pylab.array(background)
        output = Spectrum(list(wavelengths), list(corrected))
        return output
