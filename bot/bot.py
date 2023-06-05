import discord
from discord.ext import commands
from aiohttp import ClientSession
import os
from dotenv import load_dotenv
import requests

load_dotenv()
token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

async def get_info_msg():
  async with ClientSession() as session:
    async with session.get('http://bingo_server:5000/api/info_msg') as response:
      return await response.json()

@bot.slash_command(name="info", description="Get info about the bot")
async def info(ctx):
  msg = await get_info_msg()
  await ctx.respond(content=msg['content'])

@bot.command(name='teams')
async def get_teams(ctx):
    response = requests.get('http://bingo_server:5000/api/teams')
    teams = response.json()

    team_list = '\n'.join([team['display_name'] for team in teams])
    await ctx.send(f'Teams:\n{team_list}')

if __name__ == '__main__':
  bot.run(token)
