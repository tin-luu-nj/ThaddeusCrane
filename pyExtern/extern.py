"""! @brief Defines the global variables """

################################################################################
# @file extern.py
#
# @brief This file defines global variables used in whole package.
#
# @section Description
# Defines global variables used in whole package
#
# @section Libraries/Modules
# - asyncio standard library
#    + Access Lock method
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

# Import standard library
import asyncio

# gConfig contains user-configuration
gConfig = {}

# Status of Discord Bot
DiscordBotReady = False

# Discord Guild
DiscordGuild = None

# Discord Delivering message
DiscordDeliveringMsg = {}

# Discord Deliveried message
DiscordDeliveredMsg = []

# Discord Waiting to deliver message
DiscordWaitingMsg = {}

# asyncio lock system
deliverLock = asyncio.Lock()
injectLock  = asyncio.Lock()

# Manga Subscription Feed
gMangaFeed = {}

# Constant variable
DISCORD_CHANNEL_SERVER = 'server'
DISCORD_THADDEUS_CRANE_ID = 931809914559533096
################################################################################
# END OF FILE
################################################################################
