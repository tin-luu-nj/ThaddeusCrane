import disnake
from disnake.ext import commands
from pyExtern import extern

class clsListenerCog(commands.Cog):
  def __init__(self, bot) -> None:
    self.bot = bot
    self.CogReady = False

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'[INF] Listener Cog on-ready')
    if extern.DiscordGuild is not None:
      channel = disnake.utils.get(extern.DiscordGuild.text_channels, name='server')
      await channel.send(f'[NTFY]\tListener Cog loaded\n')
    self.CogReady = True

  @commands.Cog.listener()
  async def on_message(self, message):
    lMsgBufferList = extern.DiscordDeliveredMsg
    if 931809914559533096 == message.author.id and self.CogReady:
      lMsgBufferList.append(message.content)

def setup(bot):
  # print(f'[INF] Listener Cog setup')
  bot.add_cog(clsListenerCog(bot))

def teardown(bot):
  # print(f'[INF] Listener Cog teardown')
  pass

# END OF FILE
