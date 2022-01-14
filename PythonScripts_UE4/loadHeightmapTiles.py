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

gD_DebugTexture2dPath = "/Game/DebugTools/D_T_TestTexture"
gD_UseDebugTexture2d = False

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


def drawTexture2DToTexturedRenderTarget2D(iWorldContext, iTexture2dPath, iTexturedRenderTarget2DPath, iAssetName, iIntermediateAssetPath):

  unreal.log("Break-------------")
  unreal.log("Drawing Texture2d [{}] to TextureRenderTarget2D [{}]".format(iTexture2dPath, iTexturedRenderTarget2DPath ))

  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()
  render_lib = unreal.RenderingLibrary()
  material_Edit_lib = unreal.MaterialEditingLibrary()
  editor_level = unreal.EditorLevelLibrary()

  wTexture2D = editor_asset.load_asset(iTexture2dPath)
  if None == wTexture2D:
    unreal.log_error("Unable to find Debug Render Target 2D {}".format(iTexture2dPath))
    return False

  wRenderTarget2D = editor_asset.load_asset(iTexturedRenderTarget2DPath)
  if None == wRenderTarget2D:
    unreal.log_error("Unable to find Debug Render Target 2D {}".format(iTexturedRenderTarget2DPath))
    return False

  unreal.log("Break-------------")

  render_lib.clear_render_target2d(iWorldContext, wRenderTarget2D, clear_color=[0.000000, 0.000000, 0.000000, 1.000000])

  wCanvas, wSize, wDrawContext = render_lib.begin_draw_canvas_to_render_target(iWorldContext, wRenderTarget2D)

  wCanvas.draw_texture(wTexture2D,screen_position=[0.0,0.0], screen_size=wSize, coordinate_position=[0.0,0.0], coordinate_size=[1.0,1.0], render_color=[1.0,1.0,1.0,1.0], blend_mode=unreal.BlendMode.BLEND_OPAQUE )

  render_lib.end_draw_canvas_to_render_target(iWorldContext, wDrawContext)

  editor_asset.save_asset(iTexturedRenderTarget2DPath)
  return True


def drawImageFileToTexturedRenderTarget2D(iWorldContext, iImageFilePath, iTexturedRenderTarget2DPath, iAssetName, iIntermediateAssetPath):

  unreal.log("Break-------------")
  unreal.log("Drawing Texture2d [{}] to TextureRenderTarget2D [{}]".format(iTexture2dPath, iTexturedRenderTarget2DPath ))

  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  render_lib = unreal.RenderingLibrary()
  material_Edit_lib = unreal.MaterialEditingLibrary()
  editor_level = unreal.EditorLevelLibrary()

  wRenderTarget2D = editor_asset.load_asset(iTexturedRenderTarget2DPath)
  if None == wRenderTarget2D:
    unreal.log_error("Unable to find Debug Render Target 2D {}".format(iTexturedRenderTarget2DPath))
    return False

  wTexture2D = render_lib.import_file_as_texture2d(iWorldContext, iImageFilePath)
  if None == wTexture2D:
    unreal.log_error("Unable to Image To Texture 2D {}".format(iImageFilePath))
    return False


  unreal.log("Break-------------")

  render_lib.clear_render_target2d(iWorldContext, wRenderTarget2D, clear_color=[0.000000, 0.000000, 0.000000, 1.000000])

  wCanvas, wSize, wDrawContext = render_lib.begin_draw_canvas_to_render_target(iWorldContext, wRenderTarget2D)

  wCanvas.draw_texture(wTexture2D,screen_position=[0.0,0.0], screen_size=wSize, coordinate_position=[0.0,0.0], coordinate_size=[1.0,1.0], render_color=[1.0,1.0,1.0,1.0], blend_mode=unreal.BlendMode.BLEND_OPAQUE )

  render_lib.end_draw_canvas_to_render_target(iWorldContext, wDrawContext)

  editor_asset.save_asset(iTexturedRenderTarget2DPath)
  return True


# Not working, uses a material to draw texture2D on Texture Render Target 2D
def ___drawTexture2DToTexturedRenderTarget2D(iWorldContext, iTexture2dPath, iTexturedRenderTarget2DPath, iAssetName, iIntermediateAssetPath):

  unreal.log("Break-------------")
  unreal.log("Drawing Texture2d [{}] to TextureRenderTarget2D [{}]".format(iTexture2dPath, iTexturedRenderTarget2DPath ))

  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()
  render_lib = unreal.RenderingLibrary()
  material_Edit_lib = unreal.MaterialEditingLibrary()
  editor_level = unreal.EditorLevelLibrary()

  wTexture2D = editor_asset.load_asset(iTexture2dPath)
  if None == wTexture2D:
    unreal.log_error("Unable to find Texture2D {}".format(iTexture2dPath))
    return False

  wRenderTarget2D = editor_asset.load_asset(iTexturedRenderTarget2DPath)
  if None == wRenderTarget2D:
    unreal.log_error("Unable to find Texture Render Target 2D {}".format(iTexturedRenderTarget2DPath))
    return False

  unreal.log("Break-------------")

  # Create a material.
  wMaterial = None
  if True == gD_UseDebugMaterial:
    unreal.log("Using Debug material")
    wDebugMaterial = editor_asset.load_asset(gD_DebugMaterialPath)
    if None == wDebugMaterial:
      unreal.log_error("Unable to find Debug Material {}".format(gD_DebugMaterialPath))
      return False
  else:
    unreal.log("Building Render Target Material")

    wMaterialFactory = unreal.MaterialFactoryNew()
    wMaterial = asset_Tools.create_asset("M_{}".format(iAssetName), "{}/LandscapeBrush".format(iIntermediateAssetPath), unreal.Material, wMaterialFactory)

#    wMaterial.set_editor_property("blend_mode", unreal.BlendMode.BLEND_ALPHA_COMPOSITE)
    wMaterial.set_editor_property("blend_mode", unreal.BlendMode.BLEND_ADDITIVE)
    wMaterial.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)
    wMaterial.set_editor_property("allow_negative_emissive_color", True)

    wTextureSampleNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionTextureSample, -384,0)
    material_Edit_lib.connect_material_property(wTextureSampleNode, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
    wTextureSampleNode.texture = wTexture2D
    #wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
    wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
  
    wConstantNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionConstant, -384,300)
    wConstantNode.set_editor_property('R', 1.0)
    material_Edit_lib.connect_material_property(wConstantNode, "", unreal.MaterialProperty.MP_OPACITY)

    unreal.log("Saving Material")
  #  editor_asset.save_asset(wMaterial.get_path_name())
    editor_asset.save_directory(iIntermediateAssetPath)


  render_lib.clear_render_target2d(iWorldContext, wRenderTarget2D, clear_color=[0.000000, 0.000000, 0.000000, 1.000000])
  render_lib.draw_material_to_render_target(iWorldContext, wRenderTarget2D, wMaterial)

  editor_asset.save_asset(iTexturedRenderTarget2DPath)
  return True


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

  wTexture2D = None

  if True == gD_UseDebugTexture2d:
    wTexture2D = editor_asset.load_asset(gD_DebugTexture2dPath)
    if None == wTexture2D:
      unreal.log_error("Unable to find Debug Texture 2D {}".format(gD_DebugTexture2dPath))
      return False

  else:
    unreal.log("Importing Heightmap Tile as Texture : {}".format(iHeightmapTilePath))
    # Importing Heightmap Textures
    wData = unreal.AutomatedAssetImportData()
    wData.set_editor_property('destination_path', "{}/Texture2d".format(wIntermediateAssetPath))
    wData.set_editor_property('filenames', [iHeightmapTilePath])
    wList_HeightMaptexture2D = asset_Tools.import_assets_automated(wData)

    if 0 == len(wList_HeightMaptexture2D):
      unreal.log_error("Error Importing Heightmap")
      return False

    wTexture2D = wList_HeightMaptexture2D[0]
    wTexture2D.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_TERRAIN_HEIGHTMAP)
    wTexture2D.set_editor_property("compression_no_alpha", True)
    wTexture2D.set_editor_property("compression_settings", unreal.TextureCompressionSettings.TC_HALF_FLOAT)
    wTexture2D.set_editor_property("compression_quality", unreal.TextureCompressionQuality.TCQ_HIGHEST)
    wTexture2D.set_editor_property("defer_compression", True)

    unreal.log("Saving Texture2D")
    editor_asset.save_asset(wTexture2D.get_path_name())

  unreal.log("Break-------------")

  unreal.log("Creating Textured Render Target 2D")

  wTexturedRenderTarget2D = None

  if True == gD_UseDebugRenderTarget:
    wTexturedRenderTarget2D = editor_asset.load_asset(gD_DebugRenderTargetPath)
    if None == wTexturedRenderTarget2D:
      unreal.log_error("Unable to find Debug Texture Render Target 2D {}".format(gD_DebugRenderTargetPath))
      return False

  else:
    wTextureRenderTargetFactory = unreal.CanvasRenderTarget2DFactoryNew()
    wTexturedRenderTarget2D = asset_Tools.create_asset("RT_{}".format(iAssetName), "{}/HeightMapRenderTagets".format(wIntermediateAssetPath), unreal.CanvasRenderTarget2D, wTextureRenderTargetFactory)
    wTexturedRenderTarget2D.set_editor_property("size_x", gUnrealResolution[iResolutionId])
    wTexturedRenderTarget2D.set_editor_property("size_y", gUnrealResolution[iResolutionId])
    wTexturedRenderTarget2D.set_editor_property("render_target_format", unreal.TextureRenderTargetFormat.RTF_RGBA16F)
    wTexturedRenderTarget2D.set_editor_property("lod_group", unreal.TextureGroup.TEXTUREGROUP_TERRAIN_HEIGHTMAP)
    wTexturedRenderTarget2D.set_editor_property("clear_color", [0.0,0.0,0.0,1.0])

    wTexturedRenderTarget2DPath = wTexturedRenderTarget2D.get_path_name()
    editor_asset.save_asset(wTexturedRenderTarget2DPath)

    if None == wTexturedRenderTarget2D:
      unreal.log_error("Was not able to generate Textured Render Target 2D")
      return False

    unreal.log("Drawing material to Textured Render Target 2D")

    if False == drawTexture2DToTexturedRenderTarget2D(
      wWorldContext
    , wTexture2D.get_path_name()
    , wTexturedRenderTarget2DPath
    , iAssetName
    , wIntermediateAssetPath):
    
      unreal.log("Unable to Draw Textured 2D [{}] to TexturedRenderTarget2D [{}]".format(wTexture2D.get_path_name(), wTexturedRenderTarget2D.get_path_name()))
      return False
  
    editor_asset.save_asset(wTexturedRenderTarget2DPath)

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

    if True == actor.landscape_import_heightmap_from_render_target(wTexturedRenderTarget2D, import_height_from_rg_channel=True):
      unreal.log("Import Terrain Heightmap Successful")
    else:
      unreal.log_error("Import Terrain Heightmap NOT Successful")
      return False

  unreal.log("Break-------------")

  unreal.log("Saving Intermediate Folder")
  editor_asset.save_directory(wIntermediateAssetPath)

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
  deleteDirectory(iDestinationPath)

  wListOfTiles = []
  for (wDirpath, wDirnames, wFilenames) in os.walk(iHeightmapTileDirectory):
    for wCurFile in wFilenames:
        if wCurFile.endswith('.png'): 
            wListOfTiles.append([os.path.join(wDirpath, wCurFile), wCurFile])

  wHeighDirMapPath = iHeightmapTileDirectory.replace("\\", "/")
  if "/" != wHeighDirMapPath[-1]:
    wHeighDirMapPath = wHeighDirMapPath + "/"

  wNumberOfTiles = len(wListOfTiles)
  wText_label = "Importing Tiles"
  with unreal.ScopedSlowTask(wNumberOfTiles, wText_label) as slow_task:
    slow_task.make_dialog(True) 

    for wi in range(wNumberOfTiles):

      if slow_task.should_cancel():
        break

      wTilePath = wListOfTiles[wi][0]
      wTileFilename = wListOfTiles[wi][1]
      wTileRelativePath = wTilePath.replace("\\", "/").replace(wHeighDirMapPath, "./")

      slow_task.enter_progress_frame(1, desc="Processing File : {}".format(wTileRelativePath.replace("/", "\\"))) 

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

  unreal.log("Loading World Level")
  wWorldContext = loadLevel("/Game/Map/WorldMap")

  generateProjectLevelsFromHeightmap(iHeightMapTileDiretory, gOutputFolder_path, wResolutionId)
  
  unreal.log("Updating Level [WorldMap]")
  wWorldContext = loadLevel("/Game/Map/WorldMap")
  unreal.EditorLevelLibrary().save_current_level()

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
