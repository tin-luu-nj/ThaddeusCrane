from typing import Optional

import disnake
from disnake.ext import commands

class SlashCommands(commands.Cog):
  def __init__(self, bot):
    self.bot: commands.Bot = bot

  @commands.slash_command(description="Responds with 'World'")
  async def hello(inter):
    await inter.response.send_message("World")


def setup(bot):
    bot.add_cog(SlashCommands(bot))
    print(f"> Extension {__name__} is ready\n")