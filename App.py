# Site-packages
import yaml
import asyncio
import sys
import datetime
sys.tracebacklimit = 0

# Global Variable Initialization
from pyExtern import extern
with open('./config/Alfred.yml', 'r') as stream:
  extern.gConfig = yaml.load(stream, Loader=yaml.CLoader)

# Custom Library
from pyDiscordBot import DiscordBot
from pyNotificationManager import *
from pyWebScraper import MangaFeed

Alfred = DiscordBot()
MF_WebScraper = MangaFeed()

# Main Function
def main():
  try:
    Alfred.loop.create_task(continousMangaFeed()) 
    Alfred.loop.create_task(loopNotificationCheck())
    Alfred.PermanentStart()
  except KeyboardInterrupt:
    pass
  finally:
    notificationCleanup()
    print("[INF] Closing Loop")
    Alfred.loop.close()

async def notiInject():
  while True:
    if extern.DiscordBotReady:
      showtime = datetime.datetime.now()
      await notificationInject('server', 'Task 1 - Msg: {} - Time: {}'.format(extern.i, showtime))
      extern.i = extern.i + 1
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(1)

async def continousMangaFeed():
  while True:
    if MF_WebScraper.logged and extern.DiscordBotReady:
      today = str(datetime.datetime.today().date())
      await MF_WebScraper.checkFeed()

      if extern.gMangaFeed[today]['new']:
        if set(extern.gMangaFeed[today]['new']) <= set(extern.gMangaFeed[today]['notified']):
          extern.gMangaFeed[today]['new'].clear()
        else:
          pass
        for entry in extern.gMangaFeed[today]['new']:
          await notificationInject('manga-feed', f'New chapter release:\n{entry}')
          extern.gMangaFeed[today]['notified'].append(entry)
      else:
        pass

      await asyncio.sleep(1)
    else:
      await asyncio.sleep(1)

# Execution
if __name__ == '__main__':
  main()

# END OF FILE