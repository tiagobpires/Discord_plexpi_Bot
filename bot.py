import os
import subprocess
from utils import get_torrents

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name='list', help='List torrents')
async def list(ctx):
    try:
        torrents = get_torrents()
    except Exception:
        return await ctx.send('Sorry, an error occurred while processing the command.')

    if not torrents:
        return await ctx.send('No torrents in the list! You can add some using the commands.')

    columns = ['id', 'progress', 'status', 'size', 'name']

    # Calculate the max columns lengths to print the torrents info
    padding = 3
    max_column_length = {column: len(column) for column in columns}
    for torrent in torrents:
        for column in columns:
            max_length = max_column_length.get(column, 0)
            length = len(getattr(torrent, column, ''))

            if length > max_length:
                max_column_length[column] = length

    # Print the columns titles
    response = [(''.join(column.title().ljust(max_column_length.get(column, 0) + padding) for column in columns))]
    # Print the list of torrents
    for torrent in torrents:
        response.append(
            ''.join(getattr(torrent, col, '').ljust(max_column_length.get(col, 0) + padding) for col in columns)
        )

    await ctx.send('\n'.join(response))


@bot.command(name='serie', help='Download TV Series')
async def download_serie(ctx, link=''):
    if (link == ''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', os.getenv('FOLDER_SERIES')])
        await ctx.send('Downloading!')


@bot.command(name='movie', help='Download Movies')
async def download_movie(ctx, link=''):
    if (link == ''):
        await ctx.send('You must send a link.')
    else:
        subprocess.run(['transmission-remote', '-a', link, '-w', os.getenv('FOLDER_MOVIES')])
        await ctx.send('Downloading!')


@bot.command(name='remove', help="Remove torrent. Need to pass the torrent ID")
async def download_filme(ctx, id=''):
    if (id == ''):
        await ctx.send('You must send a id.')
    else:
        subprocess.run(['transmission-remote', '-t', id, '-r'])
        await ctx.send('Removed!')


# Run the bot
bot.run(TOKEN)
