##################################################################################################
# File Name: convertImageG16ToRGB8.py
# Author: Wilson Lee
#
# Purpose:
#   This script will convert image from grayscale 16bit to RGB8 format used for Unreal function "Landscape Import Heightmap from Render Target".
#
# Arguments:
#   arg 1    ImagePath or ImageDirectory (path)
#   arg 2    Destination Folder (path)
#   arg 3    Output Image Name (optional, applicable if Image Path is given)
#
##################################################################################################

import sys, os.path
from PIL import Image

def convertImage_G16ToRGB8(iImagePath, iOutputFolder, iOutputImageName=None):

  print("Converting image [{}] to RGB8 heightmap format".format(iImagePath))
  
  if None == iOutputImageName:
    iOutputImageName = os.path.splitext(os.path.basename(iImagePath))[0]

  wOutputFolderPath = iOutputFolder

  print("Output Folder [{}]".format(wOutputFolderPath))

  if False == os.path.exists(iOutputFolder):
    os.makedirs(wOutputFolderPath)

  wOriginal = Image.open(iImagePath)
  print("Input Image Mode : {}".format(wOriginal.mode))
  print("Input Image Size : {}".format(wOriginal.size))

  wChannelCount = len(wOriginal.getbands())
  print("Input Image Channel Count : {}".format(wChannelCount))

  if 1 != wChannelCount :
    print("Please Input a grayscale Image")

  wInPixels = wOriginal.load()
 
  wFloatImage = Image.new("RGB", wOriginal.size)
  wOutPixels = wFloatImage.load()

  wMax = 0
  wMin = 9999999
  for wY in range(wOriginal.size[1]):
    for wX in range(wOriginal.size[0]):
        wInR = wInPixels[wX,wY]
        if wInR > wMax:
          wMax = wInR
        if wInR < wMin:
          wMin = wInR

        wOutG = wInR % 255
        wOutR = int((wInR-wOutG)/255)
        wOutB = 255

        wOutPixels[wX, wY] = (wOutR, wOutG, wOutB)
        

  print("Max Pixel value : {}".format(wMax))
  print("Min Pixel value : {}".format(wMin))

  #wFloatImage.show()

  wFloatImage.save(os.path.join(wOutputFolderPath, "{}.png".format(iOutputImageName)))


def convertAllImageInDirectory_G16ToRGB8(iImageDirectoryPath, iOutputFolder):

  wListOfImages = []
  for (wDirpath, wDirnames, wFilenames) in os.walk(iImageDirectoryPath):
    for wCurFile in wFilenames:
        if wCurFile.endswith('.png'): 
            wListOfImages.append([os.path.join(wDirpath, wCurFile), wCurFile])
  
  for wImagePath in wListOfImages:
    convertImage_G16ToRGB8(wImagePath[0], iOutputFolder)


def main():

  wRequiredArgumentCount = 2
  wNumberOfArguments = len(sys.argv)

  wNotEnoughArguments = False

  if wRequiredArgumentCount + 1 > wNumberOfArguments:
    print("Insufficient Argument Count. Expected {}, received {}".format(wRequiredArgumentCount, wNumberOfArguments - 1))
    wNotEnoughArguments = True

  if wNotEnoughArguments:
    print("Purpose")
    print("  This script will convert image from grayscale 16bit to RGB8 format used for Unreal function \"Landscape Import Heightmap from Render Target\".")
    print("Usuage :")
    print("  argument 1 : ImagePath or ImageDirectory (path)")
    print("  argument 2 : Destination Folder (path)")
    print("  argument 3 : Output Image Name (optional, applicable if Image Path is given)")

    return

  wFilePath = sys.argv[1]    

  if False == os.path.exists(wFilePath):
    print("Error : Unable to find file [{}]".format(wFilePath))
    return

  wDestFolderPath = sys.argv[2]

  if True == os.path.isdir(wFilePath):
    convertAllImageInDirectory_G16ToRGB8(wFilePath, wDestFolderPath)
  else:

    if wNumberOfArguments > 3:
      convertImage_G16ToRGB8(wFilePath, wDestFolderPath, sys.argv[3])
    else:
      convertImage_G16ToRGB8(wFilePath, wDestFolderPath, None)

  return 

if __name__ == "__main__":
  main()