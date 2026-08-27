@echo off
SET BASE_PATH=%~dp0
echo %BASE_PATH%
support\\bin\\make.exe -C src/LADX-Origonal PYTHON=%BASE_PATH%\\support\\bin\\python.exe RGBDS=%BASE_PATH%\\support\\bin\\ azle.gbc
if errorlevel 1 goto errorhandler
support\\bin\\make.exe -C src/LADX-Hack PYTHON=%BASE_PATH%\\support\\bin\\python.exe RGBDS=%BASE_PATH%\\support\\bin\\ azle.gbc
if errorlevel 1 goto errorhandler
copy src\\LADX-Hack\\azle.gbc hack.gbc
support\\bin\\python.exe KoholintLab/ips.py src\\LADX-Origonal\\azle.gbc hack.gbc hack.ips
echo hack.gbc and hack.ips generated
pause
exit 0
:errorhandler
echo Failed...
pause
exit 1
