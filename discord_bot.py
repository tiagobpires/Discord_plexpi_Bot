# pip install -U discord.py
# pip install -U python-dotenv
import os
import subprocess
from dotenv import load_dotenv

from discord.ext import commands


# Load token from environment
load_dotenv('/home/pi/Desktop/discord.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


# Bot is ready for action
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='list', help='List torrents')
async def list(ctx):
    response = subprocess.run(['transmission-remote', '-l'], capture_output=True)
    await ctx.send(response)

@bot.command(name='serie', help='Download TV Series')
async def download_serie(ctx, link=''):
    if (link==''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', '/mnt/plexpi/torrent-complete/series'])
        await ctx.send('Downloading!')

@bot.command(name='filme', help='Download Movies')
async def download_filme(ctx, link=''):
    if (link==''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', '/mnt/plexpi/torrent-complete/filmes'])
        await ctx.send('Downloading!')

@bot.command(name='remove', help="Remove torrent. Need to put ID'torrent")
async def download_filme(ctx, id=''):
    if (id==''):
        await ctx.send('You must send a id.')
    else:
        subprocess.run(['transmission-remote', '-t', id, '-r'])
        await ctx.send('Removed!')


bot.run(TOKEN)