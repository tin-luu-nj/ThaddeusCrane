import yaml
import discord
import asyncio
from discord.ext import commands

with open('Alfred.yml', 'r') as stream:
  env = yaml.load(stream, Loader=yaml.CLoader)

TOKEN = env['server']['DISCORD_TOKEN']
GUILD = env['server']['DISCORD_GUILD']

Alfred = commands.Bot(command_prefix='!')

async def task():
  await Alfred.wait_until_ready()
  while True:
    await asyncio.sleep(1)
    print(f'[INF] Running')

def handle_exit():
  print(f'[INF] Handling')
  Alfred.loop.run_until_complete(Alfred.close())
  for t in asyncio.all_tasks(loop=Alfred.loop):
    if t.done():
      t.exception()
      continue
    t.cancel()
    try:
      Alfred.loop.run_until_complete(asyncio.wait_for(t, 5, loop=Alfred.loop))
      t.exception()
    except (asyncio.InvalidStateError,  asyncio.TimeoutError, asyncio.CancelledError):
      pass

def botInit() -> None:
  @Alfred.event
  async def on_ready():
    guild = discord.utils.get(Alfred.guilds, name=GUILD)
    print(
      f'[INF]\t{Alfred.user} is connected to the following guild:\n'
      f'\t- {guild.name}(id: {guild.id})\n'
    )

    members = '\n\t\t- '.join([member.name for member in guild.members])
    print(f'[INF]\tGuild Members:\n - {members}')

    if guild is not None:
      channel = discord.utils.get(guild.text_channels, name='server')
    await channel.send(f'📢\tAlfred is online!\n')

  @Alfred.command(name="BotStatus", pass_context=True)
  async def BotStatus(ctx):
    print(f'[INF]\t!BotStatus command received')
    await ctx.channel.send(f'📢\tHi {ctx.author.mention}, Alfred is still online')

  @Alfred.command(name="restart", pass_context=True)
  @commands.is_owner()
  async def restart(ctx):
      print(f'[WRN] Terminating')
      raise SystemExit


while True:
  botInit()
  Alfred.loop.create_task(task())
  try:
    Alfred.loop.run_until_complete(Alfred.start(TOKEN))
  except SystemExit:
    handle_exit()
  except KeyboardInterrupt:
    handle_exit()
    Alfred.loop.close()
    print('[INF] Program Ended')
    break

  print("[INF] Bot restarting")
  # Alfred = discord.Client(loop=Alfred.loop)
  Alfred = commands.Bot(command_prefix='!')
