@ECHO OFF

SET "PATH=%PATH%;%CD%\bin"
SET PYTHON39="C:\Python39\python.exe"

IF APP==%1 SET APP="%CD%\App.py"

%PYTHON39% %APP%

@ECHO ON
