import PIL
import sys
import os

import PIL.Image

#main pin code that will be used for password generation
try:
    pinCode = int(input("Input your pin code : "))
except:
    sys.exit("Pin Code is not correct")

#input the image name
fName = input("input the file name (example - file.png) : ")
fDirectory = os.path.dirname(__file__) + '/img/' + fName
if(os.path.isfile(fDirectory) == False):
    sys.exit("Image does not exist")

#trying to find the image file
with PIL.Image.open(fDirectory) as image:
    if(image.format != "PNG"):
        sys.exit("Image is not PNG")