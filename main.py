import PIL
import PIL.Image
import sys
import os

def CreateDot(currentPos, digit):
    #Just checking if this is correct !TEMP!
    print(f"Current position for dot creation : {currentPos}")
    print(image.size)

#Sets the draw pointer to a certain position, handles overflow
def MoveToNewPos(currentPos, distance):
    tempPos = [currentPos[0], currentPos[1]]
    
    #check size and currentPos against distance. overflow.
    #x
    tempPos[0] += (distance % image.size[0])
    #y
    tempPos[1] += distance // image.size[0]

    #y adding extra line if it overflows on x
    tempPos[1] += (tempPos[0]) // image.size[0]
    #x putting it in the right spot
    tempPos[0] = (tempPos[0]) % image.size[0]
    #y handling overflow
    tempPos[1] = (tempPos[1]) % image.size[1]

    return tempPos

#main pin code that will be used for password generation
pinCode = input("Input your pin code : ")

try:
    int(pinCode)
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
    
    imageMask = PIL.Image.new(mode = "RGB", size = image.size)

    currentPos = (0, 0)
    for i in range(len(str(pinCode))):
        #when even, it will sum the individual digits as distance
        if(i%2==0):
            distance = 0
            for digit in pinCode:
                distance += int(digit)
            
            #sets the position on the calculated distance
            currentPos = MoveToNewPos(currentPos, distance)
            #start drawing
            CreateDot(currentPos, int(pinCode[i]))
        #when odd, it will insert the pinCode itself as distance
        else:
            distance = int(pinCode)
            
            #sets the position on the calculated distance
            currentPos = MoveToNewPos(currentPos, distance)
            #start drawing
            CreateDot(currentPos, int(pinCode[i]))
            