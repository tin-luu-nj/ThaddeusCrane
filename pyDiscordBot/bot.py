# Get shared variable across modules
from pyExtern import extern

import asyncio
from disnake.ext import commands
from disnake.utils import get as dGet

env = extern.gConfig
TOKEN = env['discord']['bot']['token']
GUILD = env['discord']['bot']['guild']

class clsBot(commands.Bot):
  def __init__(self):
    super().__init__(command_prefix='!',
                     sync_commands=True)
    self.load_extension("pyDiscordBot.Cogs.cmdCog")
    self.load_extension("pyDiscordBot.Cogs.listenerCog")
    self.loop.create_task(self.__continuousNotify())
    self.loop.create_task(self.__continuousValidate())

  async def on_ready(self):
    extern.DiscordGuild = dGet(self.guilds, name=GUILD)
    print(
      f'[INF] {self.user} is connected to the following guild:\n'
      f'      - {extern.DiscordGuild.name} - id: {extern.DiscordGuild.id}'
    )

    if extern.DiscordGuild is not None:
      channel = dGet(extern.DiscordGuild.text_channels, name='server')
    else:
      pass

    await channel.send(f'[NTFY]\tAlfred is online!\n')
    extern.DiscordBotReady = True

  def PermanentStart(self):
    self.run(TOKEN)

  async def async_cleanup(self):
    print(f'[INF] Cleanning up')

  async def close(self):
    await self.async_cleanup()
    if extern.DiscordGuild is not None:
      channel = dGet(extern.DiscordGuild.text_channels, name='server')
    await channel.send(f'[NTFY]\tAlfred is offline!\n')
    await super().close()

  async def __continuousNotify(self):
    await self.wait_until_ready()
    while self.is_ready:
      if not extern.DiscordBotReady:
        pass
      else:
        if extern.DiscordDeliveringMsg:
          async with extern.deliverLock:
            ntfy = extern.DiscordDeliveringMsg
            if ntfy:
              for chnlNm in ntfy:
                chnl = dGet(extern.DiscordGuild.text_channels, name=chnlNm)
                for msg in ntfy[chnlNm]:
                  await chnl.send(f'{msg}')
            else:
              pass
        else:
          pass
      await asyncio.sleep(0.1)

  async def __continuousValidate(self):
    await self.wait_until_ready()
    while self.is_ready:
      if not extern.DiscordBotReady:
        pass
      else:
        async with extern.deliverLock:
          lDeliveredMsg = extern.DiscordDeliveredMsg
          if lDeliveredMsg:
            ntfy = extern.DiscordDeliveringMsg
            for chnlNm in ntfy:
              # Get common element in two list:
              # message on Discord and message in delivering file
              common = list(set(ntfy[chnlNm]).intersection(lDeliveredMsg))
              # Remove transmitted messages in delivering file
              ntfy[chnlNm] = list(set(ntfy[chnlNm])^set(common))
              # Reset validated message
              extern.DiscordDeliveredMsg.clear()
            pass
          else:
            pass
      await asyncio.sleep(0.1)

# END OF FILE
