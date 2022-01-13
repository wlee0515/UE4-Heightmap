##################################################################################################
# File Name: createHeightMapProject.py
# Author: Wilson Lee
#
# Purpose:
#   This script creates a new Unreal Engine 4.27 project with the source Heightmap.
#
# Arguments:
#   arg 1    Heightmap.png
#   arg 2    Destination folder (path)   
#   arg 3    New Project Name (str)   
#   arg 4    Tile Resolution Id (int)   
#
##################################################################################################

import sys, os, shutil, subprocess
import pathlib

gLaunchUnrealEditor = False
gUnrealResolution = [127,253,505,1009,2017,4033,8129]

gRepositoryFolder = pathlib.Path(__file__).parent.resolve()
gRepositoryFolder = os.path.abspath(gRepositoryFolder).replace("\\", "/")
gTemplateProjectPath = os.path.join(gRepositoryFolder, "Template/TemplateProject/TemplateProject.uproject").replace("\\", "/")
gPythonScriptsFolder = os.path.join(gRepositoryFolder, "PythonScripts").replace("\\", "/")
gUnrealPythonScriptsFolder = os.path.join(gRepositoryFolder, "PythonScripts_UE4").replace("\\", "/")
gPythonExe = sys.executable

gUnrealEditorCmdExe = "C:/Program Files/Epic Games/UE_4.27/Engine/Binaries/Win64/UE4Editor-Cmd.exe".replace("\\", "/")
gUnrealPyScript = os.path.join(gUnrealPythonScriptsFolder, "loadHeightmapTiles.py").replace("\\", "/")


def createHeightmapProject(iHeightmapFilePath, iDestinationFolder, iNewProjectName, iResolutionId):

  iHeightmapFilePath = os.path.abspath(iHeightmapFilePath).replace("\\", "/")
  iDestinationFolder = os.path.abspath(iDestinationFolder).replace("\\", "/")

  if ' ' in gRepositoryFolder:
    print("There are \' \' in the repository directory path. Due to limitation with the Unreal Command Line Interface, please choose a directory without \' \' in the folder path.")
    print("The repository directory path is : [{}]".format(gRepositoryFolder))
    return

  if ' ' in iDestinationFolder:
    print("There are \' \' in the Destination directory path. Due to limitation with the Unreal Command Line Interface, please choose a directory without \' \' in the folder path.")
    print("The Destination directory path is : [{}]".format(iDestinationFolder))
    return
  
  if False == os.path.isdir(iDestinationFolder):
    os.makedirs(iDestinationFolder)

  # Create Project
  wCloneProjectFilesPath = os.path.join(gPythonScriptsFolder, "cloneProjectFiles.py")
  wProcess_CloneProject = subprocess.run([gPythonExe,  wCloneProjectFilesPath, gTemplateProjectPath, iDestinationFolder, iNewProjectName])

  # Create Heightmap Tiles
  wHeightMapTileFolder = os.path.join(iDestinationFolder, "HeightmapTiles")
  wSplitImageToUnrealSizePath = os.path.join(gPythonScriptsFolder, "splitImageToUnrealSize.py")
  wProcess_SplitHeightMap = subprocess.run([gPythonExe,  wSplitImageToUnrealSizePath, iHeightmapFilePath, wHeightMapTileFolder, "{}".format(iResolutionId)])

  wProjectPath = os.path.join(iDestinationFolder, "{}/{}.uproject".format(iNewProjectName, iNewProjectName))
  wProjectPath = os.path.abspath(wProjectPath)

  # Execute Unreal Python Script
  if True == gLaunchUnrealEditor:
    wProcess_UnrealPython = subprocess.run([
      gUnrealEditorCmdExe
    , wProjectPath
    , "-ExecutePythonScript={} {} {}".format(gUnrealPyScript, wHeightMapTileFolder, "{}".format(iResolutionId))])

  else:
    wProcess_UnrealPython = subprocess.run([
      gUnrealEditorCmdExe
    , wProjectPath
    , "-stdout"
    , "-FullStdOutLogOutput"
    , "-run=pythonscript"
    , "-script={} {} {}".format(gUnrealPyScript, wHeightMapTileFolder, "{}".format(iResolutionId))])


def main():
  
  wRequiredArgumentCount = 4
  wNumberOfArguments = len(sys.argv)

  wNotEnoughArguments = False

  if wRequiredArgumentCount + 1 > wNumberOfArguments:
    print("Insufficient Argument Count. Expected {}, received {}".format(wRequiredArgumentCount, wNumberOfArguments - 1))
    wNotEnoughArguments = True

  if wNotEnoughArguments:
    print("Purpose :")
    print("  This script creates a new Unreal Engine 4.27 project with the source Heightmap.")
    print("Usuage :")
    print("  argument 1 : Heightmap.png (path")
    print("  argument 2 : Destination Folder (path)")
    print("  argument 3 : New Project Name (str) ")
    print("  argument 4 : Tile Resolution Id (int) ")
    print("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      print("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return

  wResolutionId = int(sys.argv[4])

  if len(gUnrealResolution) < wResolutionId:
    print("Error : Resolution Id not supported")
    print("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      print("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return

  return createHeightmapProject(sys.argv[1],sys.argv[2], sys.argv[3], int(sys.argv[4]))

if __name__ == "__main__":
  main()