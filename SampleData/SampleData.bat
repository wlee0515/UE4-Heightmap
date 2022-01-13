echo OFF
cls

set ENV_PROJECT_NAME="SampleDataProject"
set ENV_PROJECT_OUTPUTPATH="..\Output"
set ENV_PROJECT_IMAGE=".\Heightmap.png"
set ENV_PROJECT_RESOLUTION_ID=4
set ENV_ORIGINAL_DIRECTORY=%cd%

echo Change to script Directory
cd /D "%~dp0"

echo %cd%
echo Deleting Output Directory
del /s /f /q %ENV_PROJECT_OUTPUTPATH%\*.*
for /f %%f in ('dir /ad /b %ENV_PROJECT_OUTPUTPATH%\') do rd /s /q %ENV_PROJECT_OUTPUTPATH%\%%f

echo Starting Python Script Execution
python ..\createHeightmapProject.py %ENV_PROJECT_IMAGE% %ENV_PROJECT_OUTPUTPATH% %ENV_PROJECT_NAME% %ENV_PROJECT_RESOLUTION_ID%

echo Python Script Complete Execution

cd /D "%ENV_ORIGINAL_DIRECTORY%"
