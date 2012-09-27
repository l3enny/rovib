# Standard Libraries
import sys
import Tkinter, tkFileDialog

# Third Party Libraries
import pylab
from scipy import misc

# Local Libraries
import read

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

pylab.ion()
addressed = []
for image_path in image_paths:
    name = image_path[-8:]
    if name in addressed:
        print 'Finished!'
        break
    addressed.append(name)
    same = [i for i in image_paths if name in i]
    items = len(same)
    im = pylab.imread(same.pop(0))
    im = im.astype(pylab.float64)
    for file in same:
        next = pylab.imread(file)
        next = next.astype(pylab.float64)
        im += next
    mean = im/items
    new_im = misc.toimage(mean)
    print 'Saving to', './average/' + name
    new_im.save('./average/' + name, 'TIFF')
