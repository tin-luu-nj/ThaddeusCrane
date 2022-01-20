@SETLOCAL ENABLEDELAYEDEXPANSION
@SETLOCAL ENABLEEXTENSIONS

@ECHO OFF

SET CFG_INI=cfg.ini
SET CFG_PARSE=script\CFG_PARSING.BAT

:COMMANDCHECK
IF NOT EXIST !CFG_INI! (
  ECHO !CFG_INI! NOT EXIST
  GOTO :END
)

FOR /F "delims=" %%a IN ('CALL !CFG_PARSE! !CFG_INI! COMMAND COMMAND_LIST') DO (
  SET COMMAND_LIST=%%a
)
ECHO REQUIRED COMMAND: !COMMAND_LIST!
SET "PATH=%PATH%;%CD%\bin"
FOR %%a IN (!COMMAND_LIST!) DO (
  SET TOOL=%%a
  WHERE !TOOL! >nul 2>nul
  IF !ERRORLEVEL! NEQ 0 (
    ECHO COMMAND UNAVAILABLE: !TOOL!
    SET "CMD_UNAVAILABLE=TRUE"
  ) ELSE (
    ECHO COMMAND AVAILABLE: !TOOL!
  )
)
IF TRUE==!CMD_UNAVAILABLE! GOTO :END

:PACKAGE_DOWNLOAD
FOR /F "delims=" %%a IN ('CALL !CFG_PARSE! !CFG_INI! BINARY WGET_LIST') DO (
  SET WGET_LIST=%%a
)
FOR %%a IN (!WGET_LIST!) DO (
  SET PKG=%%a
  FOR /F "delims=" %%a IN ('CALL !CFG_PARSE! !CFG_INI! PACKAGE !PKG!') DO (
    SET FILE=%%a
  )
  IF NOT EXIST bin/!PKG! (
    IF NOT EXIST ./site-packages/!FILE! (
      FOR /F "delims=" %%a IN ('CALL !CFG_PARSE! !CFG_INI! MIRROR !FILE!') DO (
        SET LINK=%%a
      )
      ECHO DOWNLOADING: !LINK!
      wget !LINK! -P site-packages
      IF NOT EXIST ./site-packages/!FILE! (
        ECHO DOWNLOAD FAILED
      ) ELSE (
        ECHO DOWNLOAD COMPLETED
      )
    ) ELSE (
      ECHO ./site-packages/!FILE! EXIST
    )
  )
)

:TAR_PACKAGE
FOR %%a IN (!WGET_LIST!) DO (
  SET PKG=%%a
  IF NOT EXIST bin/!PKG! (
    FOR /F "delims=" %%a IN ('CALL !CFG_PARSE! !CFG_INI! PACKAGE !PKG!') DO (
      SET FILE=%%a
    )
    CD site-packages/
    tar xvfz !FILE!
    MOVE !PKG! ../bin/
    CD ..
  )
  IF NOT EXIST bin/!PKG! (
    ECHO !PKG! UNAVAILABLE
  ) ELSE (
    ECHO !PKG! AVAILABLE
  )
)

:END
ENDLOCAL
REM END OF FILE