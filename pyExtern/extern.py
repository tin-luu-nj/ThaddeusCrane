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

# counter
i = 0

# END OF FILE
