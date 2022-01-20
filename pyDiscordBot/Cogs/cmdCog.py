import disnake
from disnake.ext import commands

class clsCommandCog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print(f'[INF] Command Cog on-ready')
    guild = disnake.utils.get(self.bot.guilds, name='TheNest')
    if guild is not None:
      channel = disnake.utils.get(guild.text_channels, name='server')
      await channel.send(f'[NTFY]\tCommand Cog loaded\n')

  @commands.command(pass_context=True)
  async def status(self, ctx):
    print(f'[DBG] command received')
    await ctx.channel.send(f'[NTFY]\tHi {ctx.author.mention}, Alfred is still online')

def setup(bot):
  # print(f'[INF] Command Cog setup')
  bot.add_cog(clsCommandCog(bot))

def teardown(bot):
  # print(f'[INF] Command Cog teardown')
  pass

# END OF FILE
