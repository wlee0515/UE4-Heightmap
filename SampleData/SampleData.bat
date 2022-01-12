cls
echo Deleting Output Directory

set ENV_PROJECT_OUTPUTPATH="..\Output"

del /s /f /q %ENV_PROJECT_OUTPUTPATH%\*.*
for /f %%f in ('dir /ad /b %ENV_PROJECT_OUTPUTPATH%\') do rd /s /q %ENV_PROJECT_OUTPUTPATH%\%%f

python ..\createHeightmapProject.py ".\Heightmap.png" %ENV_PROJECT_OUTPUTPATH% "SampleData" 4