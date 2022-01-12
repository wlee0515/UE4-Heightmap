import unreal
import sys
import time

gDeleteIntermediateFiles = False
gIntermediateFolder_path = "/Game/Intermediate"
gOutputFolder_path = "/Game/Map"

gTemplateLevelPath = "/Game/TVTemplate/L_TemplateLandscape"
gHeightMapPathList = [
  "C:/Users/willee/Desktop/HeightMapTiles/map_X4_Y1_Mode_2.png"
  ,"C:/Users/willee/Desktop/HeightMapTiles/map_X4_Y1_Mode.png"
  ,"C:/Users/willee/Desktop/HeightMapTiles/map_blur_Tiles/map_blur_X6_Y2.png"
]

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
    unreal.log("Level load [{}] : Not successful".format(iLevelPath))

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
    unreal.log("Deleting Not successful [{}]".format(iDirectoryPath))


def deleteAsset(iAssetPath):
  # Instances of Unreal classes
  editor_asset = unreal.EditorAssetLibrary()
  
  unreal.log("Break-------------")
  # Clear Intermediate Files
  unreal.log("Deleting Asset [{}]".format(iAssetPath))
  if True == editor_asset.delete_asset(iAssetPath):
    unreal.log("Deleting Successful [{}]".format(iAssetPath))
  else:
    unreal.log("Deleting Not successful [{}]".format(iAssetPath))


def importTerrain(iWorldContext):

  # Instances of Unreal classes
  system_lib = unreal.SystemLibrary()
  editor_util = unreal.EditorUtilityLibrary()
  editor_level = unreal.EditorLevelLibrary()
  editor_asset = unreal.EditorAssetLibrary()
  string_lib = unreal.StringLibrary()
  render_lib = unreal.RenderingLibrary()
  material_Edit_lib = unreal.MaterialEditingLibrary()
  asset_Tools = unreal.AssetToolsHelpers.get_asset_tools()

  wIntermediateAssetPath = "{}/Maps".format(gIntermediateFolder_path)

  unreal.log("Break-------------")

  # Clear Intermediate Files
  deleteDirectory(wIntermediateAssetPath)

  unreal.log("Break-------------")

  # Importing Heightmap Textures
  wData = unreal.AutomatedAssetImportData()
  wData.set_editor_property('destination_path', "{}/HeightMaps".format(wIntermediateAssetPath))
  wData.set_editor_property('filenames', gHeightMapPathList)
  wList_HeightMaptexture2D = unreal.AssetToolsHelpers.get_asset_tools().import_assets_automated(wData)

  unreal.log("Break-------------")

  # Create a material.
  unreal.log("Building Render Target Material")

  wMaterialFactory = unreal.MaterialFactoryNew()
  wMaterial = asset_Tools.create_asset("M_LandscapeBrush", gIntermediateFolder_path, unreal.Material, wMaterialFactory)

  wMaterial.set_editor_property("blend_mode", unreal.BlendMode.BLEND_ALPHA_COMPOSITE)
  wMaterial.set_editor_property("shading_model", unreal.MaterialShadingModel.MSM_UNLIT)

  wTextureSampleNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionTextureSample, -384,0)
  material_Edit_lib.connect_material_property(wTextureSampleNode, "RGB", unreal.MaterialProperty.MP_EMISSIVE_COLOR)
  wTextureSampleNode.texture = wList_HeightMaptexture2D[0]
  #wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_COLOR)
  wTextureSampleNode.set_editor_property("sampler_type", unreal.MaterialSamplerType.SAMPLERTYPE_LINEAR_COLOR)
  
  wConstantNode = material_Edit_lib.create_material_expression(wMaterial, unreal.MaterialExpressionConstant, -384,300)
  wConstantNode.set_editor_property('R', 0.0)
  material_Edit_lib.connect_material_property(wConstantNode, "", unreal.MaterialProperty.MP_OPACITY)

  unreal.log("Saving Intermediate Folder")
  editor_asset.save_directory(gIntermediateFolder_path)

  unreal.log("Break-------------")

  # get List of Landscapes
  wLandScapeList = unreal.GameplayStatics.get_all_actors_of_class(iWorldContext, unreal.Landscape)
 
  if 0 == len(wLandScapeList):
    unreal.log("Landscape not found")
  else:
    unreal.log("Landscape was found")

  unreal.log("Number of Actors found {}".format(len(wLandScapeList)))

  for actor in wLandScapeList:

    unreal.log("Break-------------")

    unreal.log(actor)

    unreal.log("Creating Height Map texture")

    unreal.log("Creating Textured Render Target 2D")

    wTextureRenderTargetFactory = unreal.TextureRenderTargetFactoryNew()
    wTexturedRenderTarget2D = asset_Tools.create_asset("RT_{}".format(actor.get_name()), "{}/HeightMapRenderTagets".format(wIntermediateAssetPath), unreal.TextureRenderTarget2D, wTextureRenderTargetFactory)
    wTexturedRenderTarget2D.set_editor_property("size_x", 2017)
    wTexturedRenderTarget2D.set_editor_property("size_y", 2017)
    wTexturedRenderTarget2D.set_editor_property("render_target_format", unreal.TextureRenderTargetFormat.RTF_RGBA16F)
    wTexturedRenderTarget2D.set_editor_property("clear_color", [0.0,0.0,0.0,1.0])

    #wTexturedRenderTarget2D = render_lib.create_render_target2d(iWorldContext, width=2017, height=2017, format=unreal.TextureRenderTargetFormat.RTF_RGBA8, clear_color=[0.0,0.0,0.0,1.0])

    unreal.log("Drawing material to Textured Render Target 2D")

    render_lib.clear_render_target2d(iWorldContext, wTexturedRenderTarget2D, clear_color=[0.000000, 0.000000, 0.000000, 1.000000])
    render_lib.draw_material_to_render_target(iWorldContext, wTexturedRenderTarget2D, wMaterial)

    editor_asset.save_asset(wTexturedRenderTarget2D.get_path_name())
    unreal.log("Complete Drawing material to Textured Render Target 2D")

#    select_assets = editor_util.get_selected_assets()
#    if 0 != len(select_assets):
#      wTexturedRenderTarget2D = select_assets[0]


    if True == actor.landscape_import_heightmap_from_render_target(wTexturedRenderTarget2D, import_height_from_rg_channel=True):
      unreal.log("Import Terrain Heightmap Successful")
    else:
      unreal.log("Import Terrain Heightmap NOT Successful")

  unreal.log("Break-------------")

  unreal.log("Saving Intermediate Folder")
  editor_asset.save_directory(wIntermediateAssetPath)

  editor_level.save_current_level()

  
def createLandscapeActor(iWorldContext):

  # get List of Landscapes
  wLandScapeList = unreal.GameplayStatics.get_all_actors_of_class(iWorldContext, unreal.Landscape)

  wLandscapeActor = unreal.EditorLevelLibrary().spawn_actor_from_object(wLandScapeList[0].static_class(), location=[0.000000, 0.000000, 10.000000], rotation=[1.000000, 0.000000, 1.000000])
  
  unreal.log(wLandscapeActor)

def main():
  
  deleteDirectory(gIntermediateFolder_path)

  wNewLevelName = "Level_02"
  wIntermediateNewLevelPath = "{}/Sections/{}".format(gIntermediateFolder_path, wNewLevelName)
  wOutputNewLevelPath = "{}/Sections/{}".format(gOutputFolder_path, wNewLevelName)

  createLevel(wIntermediateNewLevelPath, gTemplateLevelPath)
  wWorldContext = loadLevel(wIntermediateNewLevelPath)
  #createLandscapeActor(wWorldContext)
  importTerrain(wWorldContext)
  
  deleteAsset(wOutputNewLevelPath)
  unreal.EditorAssetLibrary().duplicate_directory("/Game/Intermediate/Sections", "/Game/Map/Sections")


  wWorldContext = loadLevel("/Game/Map/FullMap")

  if True == gDeleteIntermediateFiles:
    deleteDirectory(gIntermediateFolder_path)
  return

if __name__ == "__main__" :
  wScriptFileName = sys.argv[0]
  unreal.log("Starting Script [{}]".format(wScriptFileName))

  wCount = 0
  for wArg in sys.argv:
    print("arg {} : {}".format(wCount, wArg))
    wCount = wCount + 1

  main()
  unreal.log("Ending Script [{}]".format(wScriptFileName))

