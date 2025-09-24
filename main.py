import PIL
import PIL.Image
import sys
import os

psswrdString = ""

#Draws the dot, handles everything
def CreateDot(currentPos, digit):
    if(digit > 9):
        sys.exit("Digit higher than possible was inserted")

    originCurrentPos = currentPos
    #if 0, then it's a square with a hole in the middle
    if(digit==0):
        for y in range(3):
            for x in range(3):
                if(y == 1 and x == 1):
                    currentPos = MoveToNewPosX(currentPos, 1)
                else:
                    imageMask.putpixel(currentPos, (255, 255, 255))
                    currentPos = MoveToNewPosX(currentPos, 1)
        
            currentPos = MoveToNewPos(originCurrentPos, imageMask.width*(y+1))
    #Otherwise just squares
    else:
        for y in range(digit):
            for x in range(digit):
                imageMask.putpixel(currentPos, (255, 255, 255))
                currentPos = MoveToNewPosX(currentPos, 1)
            
            currentPos = MoveToNewPos(originCurrentPos, imageMask.width*(y+1))
    
    currentPos = originCurrentPos

#Sets the draw pointer to a certain position, handles overflow
def MoveToNewPos(currentPos, distance):
    tempPos = [currentPos[0], currentPos[1]]
    
    #check size and currentPos against distance. overflow.
    #x
    tempPos[0] += (distance % image.width)
    #y
    tempPos[1] += distance // image.width

    #y adding extra line if it overflows on x
    tempPos[1] += (tempPos[0]) // image.width
    #x putting it in the right spot
    tempPos[0] = (tempPos[0]) % image.width
    #y handling overflow
    tempPos[1] = (tempPos[1]) % image.height

    return tempPos

#Sets the draw pointer to a certain position, overflow resets only X
def MoveToNewPosX(currentPos, distance):
    tempPos = [currentPos[0], currentPos[1]]

    #check size and currentPos against distance. overflow. x
    tempPos[0] += distance
    #x putting it in the right spot
    tempPos[0] = (tempPos[0]) % image.width

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
    
    #Making a copy, so that I can roll it
    copyImageMask = PIL.Image.new("RGB", imageMask.size)
    #Rolling even rows
    for y in range(imageMask.height):
        if(y%2==0):
            for x in range(imageMask.width):
                newX = (x + int(pinCode)) % imageMask.width
                pixel = imageMask.getpixel((x,y))
                copyImageMask.putpixel((newX, y), pixel)
        else:
            for x in range(imageMask.width):
                pixel = imageMask.getpixel((x,y))
                copyImageMask.putpixel((x, y), pixel)

    imageMask = copyImageMask

    #Making a copy, so that I can roll it again
    copyImageMask = PIL.Image.new("RGB", imageMask.size)
    #Rolling even columns
    for y in range(imageMask.height):
        for x in range(imageMask.width):
            if(x%2==0):
                newY = (y + int(pinCode)) % imageMask.height
                pixel = imageMask.getpixel((x,y))
                copyImageMask.putpixel((x,newY), pixel)
            else:
                pixel = imageMask.getpixel((x,y))
                copyImageMask.putpixel((x,y), pixel)
    
    imageMask = copyImageMask
    
    #pixel to character conversion
    with open("code.txt", "r") as f:
        #so we know how many chars we have to work with
        code = f.readlines()[0]
        codeLen = len(code)
        image = image.convert("RGB")

        for y in range(imageMask.height):
            for x in range(imageMask.width):
                if(imageMask.getpixel((x, y)) == (255, 255, 255)):
                   #get color data from the original image
                   r,g,b = image.getpixel((x,y))
                   colorSum = r+g+b

                   #adding char to string
                   combination = (colorSum+x+y) % codeLen
                   psswrdString = psswrdString + code[combination]

#Printing out the string by 10 chars   
lenGroupAmount = (len(psswrdString) // 10) + (len(psswrdString) % 10 != 0)
for i in range(lenGroupAmount):
    print(f"{i}: {psswrdString[i*10:(i*10)+10]}")