"""! @brief Defines the DiscordBot class """

################################################################################
# @file bot.py
#
# @brief This file defines class(es) and function(s) for pyDiscordBot.
#
# @section Description
# Defines class for pyDiscordBot
# - DiscordBot
#
# @section Libraries/Modules
# - asyncio standard library
#    + Access to sleep function
# - disnake open-source library
#    + Access commands method from extension module
#    + Access get method from utilities module
# - extern local library
#    + [RO] gConfig
#    + [RW] deliverLock
#    + [RW] DiscordGuild
#    + [RW] DiscordBotReady
#    + [RW] DiscordDeliveringMsg
#    + [RW] DiscordDeliveredMsg
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

# Import Standard Library
import asyncio

# Import open-source Library
from disnake.ext import commands
from disnake.utils import get as dGet

# Get global configuration
env = extern.gConfig
TOKEN = env['discord']['bot']['token']
GUILD = env['discord']['bot']['guild']

class clsBot(commands.Bot):
  """! The Discord Bot base class.
  Defines the base class utilized the Discord Bot.
  """
  def __init__(self) -> None:
    """! The Discord Bot class initializer.

    @param  None.
    @return  None.
    """
    # Initialization with base class
    ## command prefix: !
    ## e.g. !status
    super().__init__(command_prefix='!', sync_commands=True)
    # Load Command Cog extension
    self.load_extension("pyDiscordBot.Cogs.cmdCog")
    # Load Listener Cog extension
    self.load_extension("pyDiscordBot.Cogs.listenerCog")
    # Creat task of __continuousNotify for self instance
    self.loop.create_task(self.__continuousNotify())
    # Creat task of __continuousValidate for self instance
    self.loop.create_task(self.__continuousValidate())

  async def on_ready(self) -> None:
    """! Coroutine for on_ready event.

    @param  None.
    @return  None.
    """
    # Set global variable Guild
    extern.DiscordGuild = dGet(self.guilds, name=GUILD)
    # Print information of Discord Bot and Guild to console
    print(
      f'[INF] {self.user} is connected to the following guild:\n'
      f'      - {extern.DiscordGuild.name} - id: {extern.DiscordGuild.id}'
    )
    # Get channel 'server' in Discord Guild
    if extern.DiscordGuild is not None:
      channel = dGet(extern.DiscordGuild.text_channels, name='server')
    else:
      pass
    # Send message to Discord Guild to notify Bot is online
    await channel.send(f'[NTFY]\tAlfred is at your service!\n')
    # Set global variable Ready to True
    extern.DiscordBotReady = True

  def PermanentStart(self) -> None:
    """! Method to start Discord Bot loop initialisation.
    NOTE: ALWAYS INVOKE AT THE END OF PROGRAM,
    ALL CALLS AFTER ITS INVOCATION ARE BLOCKED.

    @param  None.
    @return  None.
    """
    # Event loop initialisation
    self.run(TOKEN)

  async def async_cleanup(self) -> None:
    """! Coroutine for clean up.

    @param  None.
    @return  None.
    """
    # Print clean-up information to console
    print(f'[INF] Cleanning up')

  async def close(self) -> None:
    """! Coroutine for closing loop event.

    @param  None.
    @return  None.
    """
    # Call async_cleanup
    await self.async_cleanup()
    # Get Discord channel 'server
    if extern.DiscordGuild is not None:
      channel = dGet(extern.DiscordGuild.text_channels, name='server')
    # Send message to Discord Guild to notify Bot is online
    await channel.send(f'[NTFY]\tAlfred is offline!\n')
    # Close class instance
    await super().close()

  async def __continuousNotify(self) -> None:
    """! Coroutine to continuous notify outbox message.

    @param  None.
    @return  None.
    """
    # Wait until Discord Bot is ready
    await self.wait_until_ready()
    # Loop forever when Bot is ready
    while self.is_ready:
      # Double check global variable for Bot Ready
      if not extern.DiscordBotReady:
        pass
      else:
        # In case there is message in outbox
        if extern.DiscordDeliveringMsg:
          # Wait for Delivery Lock
          async with extern.deliverLock:
            # Copy msg outbox to local variable
            ntfy = extern.DiscordDeliveringMsg
            # If outbox is not empty
            if ntfy:
              # Loop through each channel
              for chnlNm in ntfy:
                # Get channel
                chnl = dGet(extern.DiscordGuild.text_channels, name=chnlNm)
                # Loop through each message
                for msg in ntfy[chnlNm]:
                  # Send message to Discord Channel
                  await chnl.send(f'{msg}')
            # If outbox is empty
            else:
              pass
        # If Bot is not ready
        else:
          pass
      # Asynchronous sleep for 0.1 seconds
      await asyncio.sleep(0.1)

  async def __continuousValidate(self) -> None:
    """! Coroutine to continuous validate outbox message.

    @param  None.
    @return  None.
    """
    # Wait until Discord Bot is ready
    await self.wait_until_ready()
    # Loop forever when Bot is ready
    while self.is_ready:
      if not extern.DiscordBotReady:
        pass
      else:
        # Wait for Delivery Lock
        async with extern.deliverLock:
          # Copy sent msg to local variable
          lDeliveredMsg = extern.DiscordDeliveredMsg
          # In case there is sent message
          if lDeliveredMsg:
            # Copy msg outbox to local variable
            ntfy = extern.DiscordDeliveringMsg
            # Loop through each channel
            for chnlNm in ntfy:
              # Get common element in two list:
              # message on Discord and message in delivering file
              common = list(set(ntfy[chnlNm]).intersection(lDeliveredMsg))
              # Remove transmitted messages in delivering file
              ntfy[chnlNm] = list(set(ntfy[chnlNm])^set(common))
              # Reset validated message
              extern.DiscordDeliveredMsg.clear()
            pass
          # In case there is no sent message
          else:
            pass
      # Asynchronous sleep for 0.1 seconds
      await asyncio.sleep(0.1)

################################################################################
# END OF FILE
################################################################################
