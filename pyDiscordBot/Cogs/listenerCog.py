"""! @brief Defines the DiscordBot Event Cog """

################################################################################
# @file listener.py
#
# @brief This file defines class(es) and function(s) for pyDiscordBot.
#
# @section Description
# Defines Cog class for pyDiscordBot
# - DiscordBot
#
# @section Libraries/Modules
# - disnake open-source library
#    + Access commands method from extension module
#    + Access get method from utilities module
# - extern local library
#    + [RO] DiscordGuild
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

# Import open-source Library
from disnake.utils import get      as disnakeGet
from disnake.ext   import commands

class clsListenerCog(commands.Cog):
  """! The Event Cog base class.
  Defines the cog utilized the Discord Bot.
  """
  def __init__(self, bot) -> None:
    """! The Command Cog class initializer.

    @param[in] bot - The Bot which is using this Cog.
    @return  None.
    """
    # Set instance variable to param[in]
    self.bot = bot
    # Set CogReady to False
    self.CogReady = False

  # Decorator that marks a function as a listener
  @commands.Cog.listener()
  # Cog on_ready event
  async def on_ready(self) -> None:
    """! Coroutine for on_ready event.

    @param  None.
    @return  None.
    """
    # Print information of Discord Cog to console
    print(f'[INF] on-ready: Event Cog')
    # In case guild is available
    if extern.DiscordGuild is not None:
      # Get channel 'server'
      channel = disnakeGet(extern.DiscordGuild.text_channels, name='server')
      # Send message to Discord Guild to notify Cog is ready
      await channel.send(f'[NTFY]\ton-ready: Event Cog\n')
    # Set CogReady to True
    self.CogReady = True

  # Decorator that marks a function as a listener
  @commands.Cog.listener()
  # Cog on_message event
  async def on_message(self, message) -> None:
    """! Coroutine for on_message event.

    @param[in] message - Context in which a message is being invoked under.
    @return  None.
    """
    # Refer sent msg list to local variable
    lMsgBufferList = extern.DiscordDeliveredMsg
    # Check if message is sent by Bot
    if 931809914559533096 == message.author.id and self.CogReady:
      # Append sent msg
      lMsgBufferList.append(message.content)

def setup(bot) -> None:
  """! Method to setup Cog for Bot when loading.

  @param[in] bot - Bot which loads Cog.
  @return  None.
  """
  bot.add_cog(clsListenerCog(bot))

def teardown(bot) -> None:
  """! Method to tear down Cog for Bot when unloading.

  @param[in] bot - Bot which unload Cog.
  @return  None.
  """
  pass

################################################################################
# END OF FILE
################################################################################
