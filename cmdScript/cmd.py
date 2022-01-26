"""! @brief Application """

################################################################################
# @file App.py
#
# @brief Application.
#
# @section Description
# Application to integrate pyDiscordBot, pyNotificationManager, pyWebScraper
#
# @section Libraries/Modules
# - subprocess standard library
#    + Access to Popen method
#    + Access to PIPE constant
#
# @section NOTE
# - None
#
# @section TODO
# - None
#
# @section Change History
# Example description:
# Version Y-M-D       Author      Change description
# 1.0.0   2022-01-22  Tin Luu     Initial Version
#
# Copyright (c) 2022 Pennyworth Project.  All rights reserved.
################################################################################

# Get shared variable across modules
from pyExtern import extern

# Import standard library
from subprocess import Popen, PIPE

# Declare CONSTANT
__SCR = f'.\cmdScript\AnyDesk.cmd'

def cmdAnyDesk(cmdParam: str) -> str:
  """! Call .cmd script.

  @param - str, cmdParam - Command Parameter for AnyDesk command line.
  @return str, result of cmd script.
  """
  # UPPER CASE for cmdParam
  cmdParam = cmdParam.upper()
  # Initialize result variable
  result = 'CMD_OK'
  # In case cmdParam start with GET
  if cmdParam.startswith('GET'):
    pass
  # In case cmdParam start with SERVICE
  elif cmdParam.startswith('SERVICE'):
    # When application run with Admin right
    if not extern.IS_ADMIN:
      result = 'PERMISSION_DENIED'
    # When application NOT run with Admin right 
    else:
      pass
  # Other parameters
  else:
    result = 'INVALID_ARGUMENT'

  # When cmdParam is valid
  if 'CMD_OK' == result:
    # Invoke cmd script
    program = Popen([__SCR, cmdParam], stdout=PIPE)
    # read()          get stdout from program
    # rstrip()        remove \n\r from stdout
    # decode('UTF-8') decode byte to string
    result = program.stdout.read().rstrip().decode('UTF-8')
  else:
    pass

  # return result str
  return result

################################################################################
# END OF FILE
################################################################################
