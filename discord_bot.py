# pip install -U discord.py
# pip install -U python-dotenv

import os
import subprocess
from dotenv import load_dotenv

from discord.ext import commands


class Torrent():
    def __init__(self):
        self.id = ''
        self.name = ''
        self.size = ''
        self.status = ''
        self.progress = ''

    def __str__(self):
        return f'{self.id}\t{self.name}\t{self.size}\t{self.status}\t{self.progress}'

    def __repr__(self):
        return f'Torrent(id={self.id}, name={self.name}, size={self.size}, '\
               f'status={self.status}, progress={self.progress})'


def get_torrents():
    try:
        output = subprocess.run(['transmission-remote', '-l'], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError:
        raise Exception('Could not get the list of torrents.')

    list_str = output.stdout.split('\n')

    # Get Status and Name indexes from header
    header = list_str[0]
    columns_titles = header.split()

    # Change columns names
    columns_to_torrent = {
        'id': 'id',
        'name': 'name',
        'have': 'size',
        'status': 'status',
        'done': 'progress',
    }

    columns = {}
    for i in range(len(columns_titles)):
        column = columns_titles[i].lower()
        if column not in columns_to_torrent:
            continue

        start = header.find(columns_titles[i])
        if column == 'have':
            # Special case because of alignment of column done
            start = start - 4
        try:
            if column == 'done':
                # Special case because of alignment of column done
                end = start + 4
            else:
                end = header.find(columns_titles[i+1])
        except IndexError:
            end = None
        columns[columns_to_torrent[column]] = (start, end)

    # Remove header and footer
    list_torrents_str = list_str[1:-2]

    torrents = []
    for torrent_str in list_torrents_str:
        torrent = Torrent()
        for key, value in columns.items():
            start, end = value
            setattr(torrent, key, torrent_str[start:end].strip())
        torrents.append(torrent)

    return torrents


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
