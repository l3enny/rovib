import cPickle

import spectrum
import pylab

def generate(config_path, image_paths):
    settings = {}
    test_image = image(image_paths)
    waxis(test_image)
    regions(test_image)
    wavelengths(test_image)

    settings['waveaxis'] = test_image.waveaxis
    settings['regions'] = test_image.regions
    settings['start'] = test_image.start
    settings['end'] = test_image.end

    fid = open(config_path, 'w')
    cPickle.dump(settings, fid)
    fid.close()
    return settings

def load(config_path):
    try:
        fid = open(config_path, 'r')
        settings = cPickle.load(fid)
        print 'Settings: \n', settings, '\n'
        fid.close()
        confirm = raw_input('Configuration file detected, type \'y\' to load '
                            'the displayed settings or type \'n\' to write a '
                            'new configuration file: ')
        while True:
            if confirm is 'y':
                print '\n'
                return settings
            elif confirm is 'n':
                return None
            else:
                confirm = raw_input('Unrecognized input, please try again: ')
    except IOError:
        return None

def image(image_paths):
    test_index = raw_input('Type the index of a test image to display: ')
    while True:
        if test_index is 'y':
            break
        elif 0 <= int(test_index) <= len(image_paths):
            pylab.clf()
            test_image = spectrum.SpectrumImage(image_paths[int(test_index)])
            test_image.show()
        else:
            print 'Invalid entry, please select a number between 0 and %d' \
                  % len(image_paths)
        test_index = raw_input('Select a different image or type \'y\' to '
                               'accept the current one: ')
    return test_image

def waxis(test_image):
    waveaxis = raw_input('Please specify the wavelength axis (0 - columns, 1 - '
                         'rows): ')
    while True:
        try:
            waveaxis = int(waveaxis)
            if waveaxis is not 0 and waveaxis is not 1:
                waveaxis = raw_input('Please type \'0\' or \'1\':  ')
            else:
                test_image.waveaxis = waveaxis
                break
        except:
            waveaxis = raw_input('Please type \'0\' or \'1\':  ')
    return waveaxis

def regions(test_image):
    regiond = {'background': 0, 'data': 1}
    for (name, group) in regiond.items():
        while True:
            nregions = raw_input('How many %s regions would you like to '
                                 'specify: ' % name)
            try:
                nregions = int(nregions)
                for i in range(nregions):
                    test_image.selectregion(group)
                    test_image.drawregions(group)
                break
            except ValueError:
                nregions = raw_input('Invalid number, how many %s regions '
                                     'would you like to specify: ' % name)
    return test_image.regions

def wavelengths(test_image):
    start = raw_input('Please input the starting wavelength of the spectrum: ')
    while True:
        try:
            start = float(start)
            test_image.start = start
            break
        except ValueError:
            start = raw_input('Invalid entry, please try again: ')
    end = raw_input('Please input the ending wavelength of the spectrum: ')
    while True:
        try:
            end = float(end)
            if end > start:
                test_image.end = end
                break
        except ValueError:
            end = raw_input('Invalid entry, please try again: ')
    return start, end
