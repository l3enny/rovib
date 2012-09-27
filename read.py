import os

def find_images(path=None):
    """
    Detects images in the provided 'path' and returns a list of
    lists in the form [['path1', 'file1'], ['path2', 'file2'], ...].

    """
    if not path:
        path = '.'
    supported_types = ['.tif', '.tiff']
    images = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if os.path.splitext(file)[1] in supported_types:
                images.append(root + '/' + file)
    return images
