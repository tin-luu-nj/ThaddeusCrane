from pyExtern import extern

from os.path import exists
from os import remove
import asyncio
import yaml

async def loopNotificationCheck():
  # Loop forever
  while True:
    # When Discord Bot is ready
    if extern.DiscordBotReady:

      # When not in delivery and validation
      # When delivering dict not empty
      if extern.DiscordDeliveringMsg:
        # Get checking lock
        async with extern.deliverLock:
          # Assume all msg are delivered
          allDeliverd = True
          # Create a local copy of delivering dict
          ntfy = extern.DiscordDeliveringMsg
          # Check each channel in dict
          for chnl in ntfy:
            # In case channel is not empty, not delivered all msg yet
            if ntfy[chnl]:
              allDeliverd = False
              break
            # In case channel is empty, all msg are delivered
            else:
              pass
          # When all msg delivered, reset dict of delivering msg
          if allDeliverd:
            extern.DiscordDeliveringMsg = {}
          else:
            pass
      # When in delivery and validation
      # When delivering dict is empty
      else:
        pass

      # When dict of delivering is empty and dict of waiting is not
      if not extern.DiscordDeliveringMsg and extern.DiscordWaitingMsg:
        # Get checking lock
        async with extern.deliverLock:
          # Copy dict of waiting to dict of delivering
          # Reset dict of waiting
          extern.DiscordDeliveringMsg = dict(extern.DiscordWaitingMsg)
          extern.DiscordWaitingMsg = {}

      # When dict of delivering is not empty and/or dict of waiting is empty
      else:
        pass

    else:
      if exists('./notification/leftover.yml'):
        with open('./notification/leftover.yml', 'r') as stream:
          extern.DiscordWaitingMsg = yaml.load(stream, Loader=yaml.CLoader)
        remove('./notification/leftover.yml')
      else:
        pass

    # asynchrous sleep for 1s
    await asyncio.sleep(1)

async def notificationInject(channel, message):
  # Waiting until the lock is aquired, set it to locked and process
  async with extern.injectLock:
    # Create a local copy of waiting dict
    notif = extern.DiscordWaitingMsg
    # Create empty list if channel not exist yet
    if not channel in notif:
      notif[channel] = []
    # Append msg to channel waiting list
    notif[channel].append(message)


def notificationCleanup():
  remainingMsg = {}
  waitingMsg   = extern.DiscordWaitingMsg

  if extern.DiscordDeliveredMsg:
    ntfy = extern.DiscordDeliveringMsg
    for chnlNm in ntfy:
      # Get common element in two list:
      # message on Discord and message in delivering file
      common = list(set(ntfy[chnlNm]).intersection(extern.DiscordDeliveredMsg))
      # Remove transmitted messages in delivering file
      ntfy[chnlNm] = list(set(ntfy[chnlNm])^set(common))
      # Reset validated message
      extern.DiscordDeliveredMsg = []
    remainingMsg = dict(ntfy)
  else:
    pass

  if waitingMsg:
    for chnl in waitingMsg:
      if remainingMsg[chnl]:
        for msg in waitingMsg[chnl]:
          remainingMsg[chnl].append(msg)
      else:
        remainingMsg[chnl] = []
  else:
    pass

  if remainingMsg:
    with open('./notification/leftover.yml', 'w') as stream:
      yaml.dump(remainingMsg, stream, default_flow_style=False)
  else:
    pass
