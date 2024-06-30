@ECHO off
cls
rm test.png

setlocal enabledelayedexpansion
set imagelist=
for %%f in (*.png) do (
  set _file=%%~nf
  if [!imagelist!]==[] (
    set imagelist=!_file!.png
    ) else (
    set imagelist=!imagelist! !_file!.png
    ))
echo imgstitch.py  !imagelist!

imgstitch.py  !imagelist!

endlocal

test.png
