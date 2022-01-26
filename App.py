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
# - asyncio standard library
#    + Access to sleep method
# - datetime standard library
#    + Access today and date method in datetime class
# - sys standard library
#    + Access tracebacklimit variable
# - yaml open-source library
#    + Access to load method
#    + Access to YAML Loader "yaml.CLoader"
# - extern local library
#    + [RO] gConfig
#    + [RW] gMangaFeed
# - pyDiscordBot local library
#    + Access DiscordBot class
# - pyNotificationManager local library
#    + Access loopNotificationCheck, notificationInject,
#      notificationCleanup methods
# - pyWebscraper local library
#    + Access MangaClass class
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

# Import statndard library
import asyncio, datetime, sys
# Set traceback limit to 0
sys.tracebacklimit = 0

# Import open-source library
import yaml

# Global Variable Initialization
from pyExtern import extern
with open('./config/Alfred.yml', 'r') as stream:
  extern.gConfig = yaml.load(stream, Loader=yaml.CLoader)

# Import local library
from pyDiscordBot import DiscordBot
from pyNotificationManager import *
from pyWebScraper import MangaFeed
from cmdScript import cmdAnyDesk

# Get gloabel variable
TOKEN = extern.gConfig['discord']['bot']['token']

# Declare object
Alfred = DiscordBot()
MF_WebScraper = MangaFeed()

# Main Function
def main() -> None:
  """! Main Method.

  @param  None.
  @return  None.
  """
  # Initialize function dictionary
  if 'cmdAnyDesk' in extern.fDict:
    extern.fDict['cmdAnyDesk'] = cmdAnyDesk
  else:
    pass

  try:
    # Create Task for Alfred
    Alfred.loop.create_task(continousMangaFeed()) 
    Alfred.loop.create_task(loopNotificationCheck())
    # Start Alfred service
    # ALWAYS INVOKE AT THE END OF PROGRAM
    # ALL CALLS AFTER ITS INVOCATION ARE BLOCKED.
    Alfred.run(TOKEN)
  # Catch Keyboard Interrupt
  except KeyboardInterrupt:
    pass
  finally:
    # Cleanup notification after catch exception
    notificationCleanup()
    print("[INF] Closing Loop")
    # Close Alfred service
    Alfred.loop.close()

async def continousMangaFeed() -> None:
  """! Coroutine to continuously feed Manga Subscription news.

  @param  None.
  @return  None.
  """
  # Loop forever
  while True:
    # When Alfred is ready and Web Scraper is logged in
    if MF_WebScraper.logged and extern.DiscordBotReady:
      # Get today date
      today = str(datetime.datetime.today().date())
      # Check Manga Feed
      await MF_WebScraper.checkFeed()
      # When there is new feed
      if extern.gMangaFeed[today]['new']:
        # If new feed is subset of notified feed
        if set(extern.gMangaFeed[today]['new']) <= set(extern.gMangaFeed[today]['notified']):
          # clear new feed
          extern.gMangaFeed[today]['new'].clear()
        # If new feed is not subset of notified feed
        else:
          pass
        # Loop through each entry in new feed
        for entry in extern.gMangaFeed[today]['new']:
          # Inject new feed message to send to DiscordBot
          await notificationInject('manga-feed', f'New chapter release:\n{entry}')
          # Append entry to notified list
          extern.gMangaFeed[today]['notified'].append(entry)
      # When there is no new feed
      else:
        pass
      # Asynchronous sleep
      await asyncio.sleep(1)
    # When Alfred is not ready or Web Scraper is not logged in
    else:
      # Asynchronous sleep
      await asyncio.sleep(1)

# Execution of script
if __name__ == '__main__':
  main()

################################################################################
# END OF FILE
################################################################################
