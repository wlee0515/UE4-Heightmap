##################################################################################################
# File Name: cloneProjectFiles.py
# Author: Wilson Lee
#
# Purpose:
#   This script creates a copy of an UE4 project and renames the ".uproject" file to match folder name 
#
# Arguments:
#   arg 1    .uproject (path)   
#   arg 2    Destination folder (path)   
#   arg 3    New Project Name (path)   
#
##################################################################################################

import sys, os, shutil, re

gUnrealFoldersToCopy = [
  "Config"
  ,"Content"
  ]

  
gUnrealFoldersToDeleteFromDestination = [
  "Content\\Developers"
  ]

def cloneProjectFiles_UE4(iSourceProjectPath, iDestinationFolder, iNewProjectName):
  if False == iSourceProjectPath.endswith(".uproject"):
    print("Project file must end with \".uproject\" : ".format(iSourceProjectPath))
    return False

  if False == os.path.isfile(iSourceProjectPath):
    print("Unable to find project file : {}".format(iSourceProjectPath))
    return False
  
  if False == os.path.isdir(iDestinationFolder):
    print("Unable to find destination folder : {}".format(iDestinationFolder))
    return False

  if True == re.search(r'[^A-Za-z0-9_\-\\]',iNewProjectName):
    print("Please enter a valid Project name (A-Z, a-z, 0-9) : {}".format(iNewProjectName))
    return False

  wSourceProjectDirectory = os.path.dirname(iSourceProjectPath)
  print("Source Project directory evaluated to : {}".format(wSourceProjectDirectory))

  wDestinationProjectDirectory = os.path.join(iDestinationFolder, iNewProjectName)
  if True == os.path.isdir(wDestinationProjectDirectory):
    print("Destination Folder already exist. Please remove first : {}".format(wDestinationProjectDirectory))
    return False

  try:
    os.mkdir(wDestinationProjectDirectory)
  except OSError:
    print("Unable to create new Project directory : {}".format(wDestinationProjectDirectory))
    return False
  else:
    print("Create new project directory : {}".format(wDestinationProjectDirectory))
  
  wDestinationProjectFilePath = os.path.join(wDestinationProjectDirectory, iNewProjectName) + ".uproject"
  shutil.copyfile(iSourceProjectPath, wDestinationProjectFilePath)

  print("Created new project file : {}".format(wDestinationProjectFilePath))

  for wFolder in gUnrealFoldersToCopy:
    wSourceFolderPath = os.path.join(wSourceProjectDirectory, wFolder )
    if False == os.path.isdir(wSourceFolderPath):
      continue

    print("Copying folder : {}".format(wSourceFolderPath))

    wDestinationFolderPath = os.path.join(wDestinationProjectDirectory, wFolder )

    shutil.copytree(wSourceFolderPath, wDestinationFolderPath)

  for wFolder in gUnrealFoldersToDeleteFromDestination:
    wDestinationFolderPath = os.path.join(wDestinationProjectDirectory, wFolder )
    if False == os.path.isdir(wDestinationFolderPath):
      continue
    
    print("Removing folder : {}".format(wDestinationFolderPath))

    shutil.rmtree(wDestinationFolderPath)

  return True


def main():
  
  wRequiredArgumentCount = 3
  wNumberOfArguments = len(sys.argv)

  wNotEnoughArguments = False

  if wRequiredArgumentCount + 1 > wNumberOfArguments:
    print("Insufficient Argument Count. Expected {}, received {}".format(wRequiredArgumentCount, wNumberOfArguments - 1))
    wNotEnoughArguments = True

  if wNotEnoughArguments:
    print("Purpose :")
    print("  This script creates a copy of an UE4 project and renames the \".uproject\" file to match folder name ")
    print("Usuage :")
    print("  argument 1 : .uproject (path)")
    print("  argument 2 : Destination Folder (path)")
    print("  argument 3 : New Project Name (path) ")
    return

  return cloneProjectFiles_UE4(sys.argv[1],sys.argv[2], sys.argv[3])

if __name__ == "__main__":
  main()