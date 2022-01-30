@ECHO OFF

pyinstaller -F App.py
MOVE .\dist\App.exe .\Pennyworth.exe
RMDIR /S /Q .\dist
RMDIR /S /Q .\build
DEL /S /Q App.spec

@ECHO ON
