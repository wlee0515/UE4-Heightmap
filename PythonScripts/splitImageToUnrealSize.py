##################################################################################################
# File Name: splitImageToUnrealSize.py
# Author: Wilson Lee
#
# Purpose:
#   This script splits an image to the recommended heightmap Size provided by Unreal.
#
# Arguments:
#   arg 1    ImagePath (path)
#   arg 2    Destination Folder (path)
#   arg 3    Tile Resolution Id (int)   
#   arg 4    Keep Partial Tiles (int 1 = True) (Optional)   
#
##################################################################################################

import sys, os.path
from PIL import Image


gUnrealResolution = [127,253,505,1009,2017,4033,8129]


def splitImage(iImagePath, iOutputFolder, iWidth, iHeight, iSkipIncompleteTiles):
  print("Splitting image [{}] into {} x {} size tiles".format(iImagePath, iWidth, iHeight))
  if True == iSkipIncompleteTiles:
    print("Skipping Incomplete Tiles")

  wImageName = os.path.splitext(os.path.basename(iImagePath))[0]

  wOutputFolderPath = iOutputFolder

  print("Output Folder [{}]".format(wOutputFolderPath))

  if False == os.path.exists(iOutputFolder):
    os.makedirs(wOutputFolderPath)

  wOriginal = Image.open(iImagePath)
  #wOriginal.show()


  wImageWidth, wImageHeight = wOriginal.size   # Get dimensions

  wYMax = 0
  for wj in range(0, wImageHeight, iHeight):
    wBottom = wj + iHeight
    if wBottom > wImageHeight:
      if True == iSkipIncompleteTiles:
        break
    wYMax = wYMax + 1
  wYMax = wYMax - 1

  wXCount = 0
  for wi in range(0, wImageWidth, iWidth):
    wYCount = wYMax
    for wj in range(0, wImageHeight, iHeight):
      wLeft = wi
      wRight = wi + iWidth
      if wRight > wImageWidth:
        wRight = wImageWidth
        if True == iSkipIncompleteTiles:
          continue

      wTop = wj
      wBottom = wj + iHeight
      if wBottom > wImageHeight:
        wBottom = wImageHeight
        if True == iSkipIncompleteTiles:
          continue

      wSubSection = wOriginal.crop((wLeft, wTop, wRight, wBottom))
      
      #wSubSection.show()
      wOutputFileName = "{}_X{}_Y{}.png".format(wImageName, wXCount, wYCount)
      wOutputFilePath = os.path.join(wOutputFolderPath,wOutputFileName)
      wSubSection.save(wOutputFilePath)
    
      wYCount = wYCount - 1
    wXCount = wXCount + 1


def main():

  wRequiredArgumentCount = 3
  wNumberOfArguments = len(sys.argv)

  wNotEnoughArguments = False

  if wRequiredArgumentCount + 1 > wNumberOfArguments:
    print("Insufficient Argument Count. Expected {}, received {}".format(wRequiredArgumentCount, wNumberOfArguments - 1))
    wNotEnoughArguments = True

  if wNotEnoughArguments:
    print("Usuage :")
    print("  argument 1 : ImagePath (path)")
    print("  argument 2 : Destination Folder (path)")
    print("  argument 3 : Tile Resolution Id (int)")
    print("  argument 4 : Keep Partial Tiles (int 1 = True) (Optional)")
    print("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      print("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return


  wFilePath = sys.argv[1]    

  if False == os.path.exists(wFilePath):
    print("Error : Unable to find file [{}]".format(wFilePath))
    return

  wDestFolderPath = sys.argv[2]

  wResolutionId = int(sys.argv[3])

  if len(gUnrealResolution) < wResolutionId:
    print("Error : Resolution Id not supported")
    print("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      print("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return

  wSkipPartialTiles = True
  if len(sys.argv) > 4:
    if 1 == int(sys.argv[4]):
      wSkipPartialTiles = False

  return splitImage(wFilePath, wDestFolderPath, gUnrealResolution[wResolutionId], gUnrealResolution[wResolutionId], wSkipPartialTiles)
  

if __name__ == "__main__":
  main()