cls
echo Deleting Output Directory

del /s /f /q ..\Output\*.*
for /f %%f in ('dir /ad /b ..\Output\') do rd /s /q ..\Output\%%f

python ..\createHeightmapProject.py ".\Heightmap.png" "..\Output" "SampleData" 4