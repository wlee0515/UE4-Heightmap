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

gRepositoryFolder = pathlib.Path(__file__).parent.resolve()
gRepositoryFolder = str(gRepositoryFolder).replace("\\", "/")
gTemplateProjectPath = os.path.join(gRepositoryFolder, "Template/TemplateProject/TemplateProject.uproject")
gPythonScriptsFolder = os.path.join(gRepositoryFolder, "PythonScripts")
gUnrealPythonScriptsFolder = os.path.join(gRepositoryFolder, "PythonScripts_UE4")
gPythonExe = sys.executable

gUnrealEditorCmdExe = "C:/Program Files/Epic Games/UE_4.27/Engine/Binaries/Win64/UE4Editor-Cmd.exe"
gUnrealPyScript = os.path.join(gUnrealPythonScriptsFolder, "loadHeightMap.py")

gUnrealResolution = [127,253,505,1009,2017,4033,8129]

def createHeightmapProject(iHeightmapFilePath, iDestinationFolder, iNewProjectName, iResolutionId):
  # Create Project
  wCloneProjectFilesPath = os.path.join(gPythonScriptsFolder, "cloneProjectFiles.py")
  wProcess_CloneProject = subprocess.run([gPythonExe,  wCloneProjectFilesPath, gTemplateProjectPath, iDestinationFolder, iNewProjectName])

  # Create Heightmap Tiles
  wHeightMapTileFolder = os.path.join(iDestinationFolder, "HeightmapTiles")
  wSplitImageToUnrealSizePath = os.path.join(gPythonScriptsFolder, "splitImageToUnrealSize.py")
  wProcess_SplitHeightMap = subprocess.run([gPythonExe,  wSplitImageToUnrealSizePath, iHeightmapFilePath, wHeightMapTileFolder, "{}".format(iResolutionId)])

  # Execute Unreal Python Script
  wProjectPath = os.path.join(iDestinationFolder, "{}/{}.uproject".format(iNewProjectName, iNewProjectName))
  wProjectPath = os.path.abspath(wProjectPath)
  wProcess_UnrealPython = subprocess.run([
    gUnrealEditorCmdExe
  , wProjectPath
  , "-stdout"
  , "-FullStdOutLogOutput"
  , "-run=pythonscript"
  , "-script=\"{}\"".format(gUnrealPyScript, wHeightMapTileFolder)])

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