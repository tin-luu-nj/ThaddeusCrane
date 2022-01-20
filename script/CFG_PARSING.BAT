@SETLOCAL ENABLEDELAYEDEXPANSION
@SETLOCAL ENABLEEXTENSIONS

@ECHO OFF
SET file=%~1
SET section=[%~2]
SET key=%~3
SET currentSection=
FOR /f "usebackq delims=" %%a IN ("!file!") DO (
  SET ln=%%a
  IF "x!ln:~0,1!"=="x[" (
    SET currentSection=!ln!
  ) ELSE (
    FOR /f "tokens=1,2 delims==" %%b IN ("!ln!") DO (
      SET currentKey=%%b
      SET currentVal=%%c
      IF "x!section!"=="x!currentSection!" IF "x!key!"=="x!currentKey!" (
        ECHO !currentVal!
      )
    )
  )
)

ENDLOCAL