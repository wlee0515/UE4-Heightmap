##################################################################################################
# File Name: loadHeightmapTiles.py
# Author: Wilson Lee
#
# Purpose:
#   This script will create a new level (.umap) for every heightmap tile from the given directory
#
# Arguments:
#   arg 1    Heightmap Tile Directory (path)
#   arg 2    Tile Resolution Id (int)   
#
##################################################################################################

import unreal
import sys
import os
import time
import shutil

gUnrealResolution = [127,253,505,1009,2017,4033,8129]

gDeleteIntermediateFiles = False
gIntermediateFolder_path = "/Game/Intermediate"
gOutputFolder_path = "/Game/Map/Sections"

gD_DebugMaterialPath = "/Game/DebugTools/D_M_TestMaterial"
gD_UseDebugMaterial = False

gD_DebugRenderTargetPath = "/Game/DebugTools/D_RT_MaterialTest"
gD_UseDebugRenderTarget = False


def createLevel(wNewLevelPath, iTemplateLevelPath):
  # Instances of Unreal classes
  editor_level = unreal.EditorLevelLibrary()
  return editor_level.new_level_from_template(wNewLevelPath, iTemplateLevelPath)


def moveLevelAssets(iOldPathDir, iNewPathDir):
  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  editor_asset.rename_directory(iOldPathDir, iNewPathDir)


def loadLevel(iLevelPath):

  # Instances of Unreal classes
  editor_level = unreal.EditorLevelLibrary()

  unreal.log("Break-------------")
  # Load Level
  if True == editor_level.load_level(iLevelPath):
    unreal.log("Level load [{}] : Successful".format(iLevelPath))
  else:
    unreal.log_error("Level load [{}] : Not successful".format(iLevelPath))

  # get World Context, must be after loading level
  wWorld = unreal.EditorLevelLibrary.get_editor_world()
  return wWorld


def saveLevel():  
  # Instances of Unreal classes
  editor_level = unreal.EditorLevelLibrary()
  editor_level.save_current_level()


def deleteDirectory(iDirectoryPath):
  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()

  unreal.log("Break-------------")
  # Clear Intermediate Files
  unreal.log("Deleting Asset Folder [{}]".format(iDirectoryPath))
  if True == editor_asset.delete_directory(iDirectoryPath):
    unreal.log("Deleting Successful [{}]".format(iDirectoryPath))
  else:
    unreal.log_error("Deleting Not successful [{}]".format(iDirectoryPath))
  
  if True == os.path.isdir(iDirectoryPath):
    shutil.rmtree(iDirectoryPath)


def deleteAsset(iAssetPath):
  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  
  unreal.log("Break-------------")
  # Clear Intermediate Files
  unreal.log("Deleting Asset [{}]".format(iAssetPath))
  if True == editor_asset.delete_asset(iAssetPath):
    unreal.log("Deleting Successful [{}]".format(iAssetPath))
  else:
    unreal.log_error("Deleting Not successful [{}]".format(iAssetPath))


def loadHeightmapIntoLevel(iHeightmapTilePath, iLevelPath, iAssetName, iResolutionId):

  wIntermediateAssetPath = "{}/Maps".format(gIntermediateFolder_path)

  # Instances of Unreal classes
  editor_level = unreal.EditorLevelLibrary()
  editor_asset = unreal.EditorAssetLibrary()
  asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()
  material_Edit_lib = unreal.MaterialEditingLibrary()
  render_lib = unreal.RenderingLibrary()

  unreal.log("Break-------------")
  # Load Level
  if True == editor_level.load_level(iLevelPath):
    unreal.log("Level load [{}] : Successful".format(iLevelPath))
  else:
    unreal.log_error("Level load [{}] : Not successful".format(iLevelPath))

  # get World Context, must be after loading level
  wWorldContext = editor_level.get_editor_world()

  unreal.log("Break-------------")

  unreal.log("Importing Heightmap Tile as Texture : {}")
  # Importing Heightmap Textures
  wData = unreal.AutomatedAssetImportData()
  wData.set_editor_property('destination_path', "{}/Texture2d".format(wIntermediateAssetPath))
  wData.set_editor_property('filenames', [iHeightmapTilePath])
  wList_HeightMaptexture2D = asset_Tools.import_assets_automated(wData)

  if 0 == len(wList_HeightMaptexture2D):
    unreal.log_error("Error Importing Heightmap")
    return False

  unreal.log("Saving Texture2D")
  editor_asset.save_asset(wList_HeightMaptexture2D[0].get_path_name())

  unreal.log("Break-------------")

  # Create a material.
  unreal.log("Building Render Target Material")

  wMaterialFactory = unreal.MaterialFactoryNew()
  wMaterial = asset_Tools.create_asset("M_{}".format(iAssetName), "{}/LandscapeBrush".format(wIntermediateAssetPath), unreal.Material, wMaterialFactory)

  wMaterial.set_editor_property("blend_mode", unreal.BlendMode.BLEND_ALPHA_COMPOSITE)
  wMaterial.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)

  wTextureSampleNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionTextureSample, -384,0)
  material_Edit_lib.connect_material_property(wTextureSampleNode, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
  wTextureSampleNode.texture = wList_HeightMaptexture2D[0]
  #wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
  wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
  
  wConstantNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionConstant, -384,300)
  wConstantNode.set_editor_property('R', 1.0)
  material_Edit_lib.connect_material_property(wConstantNode, "", unreal.MaterialProperty.MP_OPACITY)

  unreal.log("Saving Material")
  editor_asset.save_asset(wMaterial.get_path_name())

  unreal.log("Break-------------")

  # get List of Landscapes
  wLandScapeList = unreal.GameplayStatics.get_all_actors_of_class(wWorldContext, unreal.Landscape)
 
  if 0 == len(wLandScapeList):
    unreal.log_error("Landscape not found")
    return False
  else:
    unreal.log("Landscape was found")

  unreal.log("Number of Actors found {}".format(len(wLandScapeList)))

  for actor in wLandScapeList:

    unreal.log("Break-------------")

    unreal.log(actor)

    unreal.log("Creating Textured Render Target 2D")

    wTexturedRenderTarget2D = None

    if True == gD_UseDebugRenderTarget:
      wTexturedRenderTarget2D = editor_asset.load_asset(gD_DebugRenderTargetPath)
      if None == wTexturedRenderTarget2D:
        unreal.log_error("Unable to find Debug Render Target 2D {}".format(gD_DebugRenderTargetPath))
        return False

    else:
      wTextureRenderTargetFactory = unreal.TextureRenderTargetFactoryNew()
      wTexturedRenderTarget2D = asset_Tools.create_asset("RT_{}_{}".format(iAssetName, actor.get_name()), "{}/HeightMapRenderTagets".format(wIntermediateAssetPath), unreal.TextureRenderTarget2D, wTextureRenderTargetFactory)
      wTexturedRenderTarget2D.set_editor_property("size_x", gUnrealResolution[iResolutionId])
      wTexturedRenderTarget2D.set_editor_property("size_y", gUnrealResolution[iResolutionId])
      wTexturedRenderTarget2D.set_editor_property("render_target_format", unreal.TextureRenderTargetFormat.RTF_RGBA16F)
      wTexturedRenderTarget2D.set_editor_property("clear_color", [0.0,0.0,0.0,1.0])

      if None == wTexturedRenderTarget2D:
        unreal.log_error("Was not able to generate Textured Render Target 2D")
        return False

      unreal.log("Drawing material to Textured Render Target 2D")

      render_lib.clear_render_target2d(wWorldContext, wTexturedRenderTarget2D, clear_color=[0.000000, 0.000000, 0.000000, 1.000000])

      if True == gD_UseDebugMaterial:
        wDebugMaterial = editor_asset.load_asset(gD_DebugMaterialPath)
        if None == wDebugMaterial:
          unreal.log_error("Unable to find Debug Material {}".format(gD_DebugMaterialPath))
          return False
        else:
          render_lib.draw_material_to_render_target(wWorldContext, wTexturedRenderTarget2D, wDebugMaterial)        
      else:
        render_lib.draw_material_to_render_target(wWorldContext, wTexturedRenderTarget2D, wMaterial)

      editor_asset.save_asset(wTexturedRenderTarget2D.get_path_name())
      unreal.log("Complete Drawing material to Textured Render Target 2D")

    if True == actor.landscape_import_heightmap_from_render_target(wTexturedRenderTarget2D, import_height_from_rg_channel=True):
      unreal.log("Import Terrain Heightmap Successful")
    else:
      unreal.log_error("Import Terrain Heightmap NOT Successful")
      return False

  unreal.log("Break-------------")
  unreal.log("Saving Level {}".format(iLevelPath))
  editor_level.save_current_level()
  return True


def generateProjectLevelForTile(iHeightmapTilePath, iDestinationPath, iResolutionId):

  wImageName = os.path.splitext(os.path.basename(iHeightmapTilePath))[0]
  wImageName = wImageName.replace(" ", "_")

  wTemplateLevelPath = "/Game/Template/L_Template_{}".format(gUnrealResolution[iResolutionId])
  wNewLevelPath = iDestinationPath + "/L_{}".format(wImageName)

  if False == createLevel(wNewLevelPath, wTemplateLevelPath):
    unreal.log_error("Unable to create Level for Image : {}".format(iHeightmapTilePath))
    unreal.log_error("Exiting Task")
    return

  return loadHeightmapIntoLevel(iHeightmapTilePath, wNewLevelPath, wImageName, iResolutionId)


def generateProjectLevelsFromHeightmap(iHeightmapTileDirectory, iDestinationPath, iResolutionId):
  deleteDirectory(gIntermediateFolder_path)

  wListOfTiles = []
  for (wDirpath, wDirnames, wFilenames) in os.walk(iHeightmapTileDirectory):
    for wCurFile in wFilenames:
        if wCurFile.endswith('.png'): 
            wListOfTiles.append(os.path.join(wDirpath, wCurFile))

  wNumberOfTiles = len(wListOfTiles)
  wText_label = "Importing Tiles"
  with unreal.ScopedSlowTask(wNumberOfTiles, wText_label) as slow_task:
    slow_task.make_dialog(True) 
    for wi in range(wNumberOfTiles):
      if slow_task.should_cancel():
        break
      wTilePath = wListOfTiles[wi]
      slow_task.enter_progress_frame(1, desc="Processing File : {}".format(wTilePath)) 
      if False == generateProjectLevelForTile(wTilePath, iDestinationPath, iResolutionId):
        unreal.log_error("Error loading heightmap into level for Tile {}".format(wTilePath))
        unreal.log_error("Exiting Batch Task")
        return False


  if True == gDeleteIntermediateFiles:
    deleteDirectory(gIntermediateFolder_path)
  return True


def main():

  wRequiredArgumentCount = 2
  wNumberOfArguments = len(sys.argv)

  wNotEnoughArguments = False

  if wRequiredArgumentCount + 1 > wNumberOfArguments:
    unreal.log_error("Insufficient Argument Count. Expected {}, received {}".format(wRequiredArgumentCount, wNumberOfArguments - 1))
    wNotEnoughArguments = True

  if wNotEnoughArguments:
    unreal.log("Purpose")
    unreal.log("  This script will create a new level (.umap) for every heightmap tile from the given directory.")
    unreal.log("Usuage :")
    unreal.log("  argument 1 : Heightmap Tile Directory (path)")
    unreal.log("  argument 2 : Tile Resolution Id (int)")
    unreal.log("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      unreal.log("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return

  iHeightMapTileDiretory = sys.argv[1]    

  if False == os.path.exists(iHeightMapTileDiretory):
    unreal.log("Error : Unable to find file [{}]".format(iHeightMapTileDiretory))
    return

  wResolutionId = int(sys.argv[2])

  if len(gUnrealResolution) < wResolutionId:
    unreal.log("Error : Resolution Id not supported")
    unreal.log("Supported Id's are :")
    for wi in range(0, len(gUnrealResolution)):
      unreal.log("  {} for {} x {}".format(wi, gUnrealResolution[wi], gUnrealResolution[wi]))
    return

  generateProjectLevelsFromHeightmap(iHeightMapTileDiretory, gOutputFolder_path, wResolutionId)
  
  unreal.log("Loading World Level")
  wWorldContext = loadLevel("/Game/Map/WorldMap")
  
  return 

  

if __name__ == "__main__":
  
  wScriptFileName = sys.argv[0]
  unreal.log("Starting Script [{}]".format(wScriptFileName))

  wCount = 0
  for wArg in sys.argv:
    unreal.log("arg {} : {}".format(wCount, wArg))
    wCount = wCount + 1

  main()
  unreal.log("Ending Script [{}]".format(wScriptFileName))
