# pip install -U discord.py
# pip install -U python-dotenv

import os
import subprocess
from dotenv import load_dotenv

from discord.ext import commands


# Makes torrent list more presentable
def process_list_torrent(input):

    # List of input words
    list = str(input).split()

    # Processed text initialized with the header
    output = 'Id     Done     Status     Nome\n'

    # List length removing unimportant text from the end
    list_length = len(list) - 7

    # Run through each torrent
    for i in range(12, list_length, 10):

        # Concatenate output and torrent information
        output += list[i] + '      ' + list[i+1] + '     ' + list[i+8] + '    ' + list[i+9] + '\n'

    return output


# Load token from environment
load_dotenv('/home/pi/Desktop/discord.env')
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


# Bot is ready for action
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    
# Comands:
# List all torrents
@bot.command(name='list', help='List torrents')
async def list(ctx):
    list_torrent = subprocess.run(['transmission-remote', '-l'], capture_output=True)
    response = process_list_torrent(list_torrent)
    
    await ctx.send(response)

# Download TV Series
@bot.command(name='serie', help='Download TV Series')
async def download_serie(ctx, link=''):
    if (link==''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', '/mnt/plexpi/torrent-complete/series'])
        await ctx.send('Downloading!')

# Download Movies
@bot.command(name='movie', help='Download Movies')
async def download_movie(ctx, link=''):
    if (link==''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', '/mnt/plexpi/torrent-complete/filmes'])
        await ctx.send('Downloading!')

# Remove Torrent
@bot.command(name='remove', help="Remove torrent. Need to put ID'torrent")
async def download_filme(ctx, id=''):
    if (id==''):
        await ctx.send('You must send a id.')
    else:
        subprocess.run(['transmission-remote', '-t', id, '-r'])
        await ctx.send('Removed!')

# Run bot
bot.run(TOKEN)
