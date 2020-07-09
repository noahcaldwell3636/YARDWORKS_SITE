from os import listdir, rename
from os.path import isfile, join
from PIL import Image, ExifTags

mypath = "C:/Users/ncaldwell/Documents/Source Code/YW_Site/YW_site/static/photos/equipment"
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

if __name__ == "__main__":
    for f in onlyfiles:
        filepath = join(mypath, f)
        rotate_image(filepath)