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

Alfred = DiscordBot()

# Main Function
def main():
  try:
    Alfred.loop.create_task(notiInject_1())
    Alfred.loop.create_task(notiInject_2())
    Alfred.loop.create_task(notiInject_3())
    Alfred.loop.create_task(loopNotificationCheck())
    Alfred.PermanentStart()
  except KeyboardInterrupt:
    pass
  finally:
    notificationCleanup()
    print("[INF] Closing Loop")
    Alfred.loop.close()
    # loop.close()

async def notiInject_1():
  while True:
    if extern.DiscordBotReady:
      showtime = datetime.datetime.now()
      await notificationInject('server', 'Task 1 - Msg: {} - Time: {}'.format(extern.i, showtime))
      extern.i = extern.i + 1
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(1)

async def notiInject_2():
  while True:
    if extern.DiscordBotReady:
      showtime = datetime.datetime.now()
      global i
      await notificationInject('server', 'Task 2 - Msg: {} - Time: {}'.format(extern.i, showtime))
      extern.i = extern.i + 1
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(1)

async def notiInject_3():
  while True:
    if extern.DiscordBotReady:
      showtime = datetime.datetime.now()
      global i
      await notificationInject('server', 'Task 3 - Msg: {} - Time: {}'.format(extern.i, showtime))
      extern.i = extern.i + 1
      await asyncio.sleep(1)
    else:
      await asyncio.sleep(1)
  
# Execution
if __name__ == '__main__':
  main()

# END OF FILE