"""! @brief Defines the method of Notification Manager """

################################################################################
# @file bot.py
#
# @brief This file defines class(es) and function(s) for pyNotificatioManager.
#
# @section Description
# Defines class for pyNotificatioManager
# - loopNotificationCheck
# - notificationInject
# - notificationCleanup
#
# @section Libraries/Modules
# - asyncio standard library
#    + Access to sleep method
# - os standard library
#    + Access to exists method in path module
#    + Access to remove method
# - yaml standard library
#    + Access to load, dump method
#    + Access to YAML Loader "yaml.CLoader"
# - extern local library
#    + [RW] deliverLock
#    + [RW] DiscordBotReady
#    + [RW] DiscordDeliveringMsg
#    + [RW] DiscordDeliveredMsg
#    + [RW] DiscordWaitingMsg
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
from os.path import exists
from os import remove

# Import open-source library
import asyncio, yaml

async def loopNotificationCheck() -> None:
  """! Coroutine for loop to checking notification.

  @param  None.
  @return  None.
  """
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

    # When Discord Bot is not ready
    # i.e. initialization of Bot
    else:
      # When leftover.yml is exist
      if exists('./notification/leftover.yml'):
        # Open leftover.yml as standard input stream
        with open('./notification/leftover.yml', 'r') as stream:
          # Load leftover.yml to outbox
          extern.DiscordWaitingMsg = yaml.load(stream, Loader=yaml.CLoader)
        # Remove leftover.yml
        remove('./notification/leftover.yml')
      # When leftover.yml is not exist
      else:
        pass

    # asynchrous sleep for 1s
    await asyncio.sleep(1)

async def notificationInject(channel, message):
  """! Coroutine to inject notification.

  @param[in] message - The outboxing message.
  @return None.
  """
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
  """! Coroutine to clean-up notification.

  @param None.
  @return None.
  """
  # Declare local variables
  remainingMsg = {}
  waitingMsg   = extern.DiscordWaitingMsg

  # When there is sent messages
  if extern.DiscordDeliveredMsg:
    # Refer global variable to local variable
    ntfy = extern.DiscordDeliveringMsg
    # Loop through each channel
    for chnlNm in ntfy:
      # Get common element in two list:
      # message on Discord and message in delivering file
      common = list(set(ntfy[chnlNm]).intersection(extern.DiscordDeliveredMsg))
      # Remove transmitted messages in delivering file
      ntfy[chnlNm] = list(set(ntfy[chnlNm])^set(common))
      # Reset validated message
      extern.DiscordDeliveredMsg.clear()
    # Create a copy dictionary of notification to remaining message
    remainingMsg = dict(ntfy)
  # When there is no sent message
  else:
    # Do nothing
    pass

  # When there is outboxing message
  if waitingMsg:
    # Loop through each channel
    for chnl in waitingMsg:
      # When channel containing remaining message
      if remainingMsg[chnl]:
        # Loop through each message
        for msg in waitingMsg[chnl]:
          # Append message to remaining message list
          remainingMsg[chnl].append(msg)
      # When channel not containing remaining message
      else:
        #  Clear remaining message list
        remainingMsg[chnl].clear()
  # When there is no outboxing message
  else:
    # Do nothing
    pass

  # When there is remaining messages
  if remainingMsg:
    # Open leftover.yml as standard input stream
    with open('./notification/leftover.yml', 'w') as stream:
      # Dump remaining message to output file
      yaml.dump(remainingMsg, stream, default_flow_style=False)
  # When there is no remaining messages
  else:
    # Do nothing
    pass

  # When existed MangaFeed
  if extern.gMangaFeed:
    # Open manga-feed.yml as standard input stream
    with open('./notification/manga-feed.yml', 'w') as stream:
      # Dump manga feed to output file
      yaml.dump(extern.gMangaFeed, stream, default_flow_style=False)
  else:
    # Do nothing
    pass

################################################################################
# END OF FILE
################################################################################
