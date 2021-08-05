import os
import subprocess
from utils import get_emoji, get_torrents, switch_emojis

from dotenv import load_dotenv
from discord.ext import commands


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} is alive!')


@bot.command(help='Check if the bot is listening')
async def ping(ctx):
    await ctx.send(':ping_pong: Pong!')


@bot.command(aliases=['emojis'], help='Switch the emojis use')
async def emoji(ctx):
    return await ctx.send(switch_emojis())


@bot.command(aliases=['listar'], help='List torrents')
async def list(ctx):
    try:
        torrents = get_torrents()
    except Exception:
        return await ctx.send('Sorry, an error occurred while processing the command.' + get_emoji('bad'))

    if not torrents:
        return await ctx.send('No torrents in the list! You can add some using the commands.' + get_emoji('good'))

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


async def download(ctx, folder=None, *links):
    if not links:
        return await ctx.send('You must send at least one torrent link.' + get_emoji())

    specify_folder = ['-w', folder] if folder else []

    for count, link in enumerate(links, start=1):
        link_number = f'{count}º ' if len(links) > 1 else ''
        try:
            subprocess.run(['transmission-remote', '-a', link] + specify_folder, check=True)
        except subprocess.CalledProcessError:
            await ctx.send(f'The {link_number}link is invalid or a corrupted torrent.' + get_emoji('bad'))
        else:
            await ctx.send(f'Downloading {link_number}link!' + get_emoji('good'))

    if len(links) > 1:
        await ctx.send(get_emoji('good'))


@bot.command(aliases=['series', 'série', 'séries'], help='Download TV Series. You can send multiple links.')
async def serie(ctx, *links):
    folder = os.getenv('FOLDER_SERIES')
    await download(ctx, folder, *links)


@bot.command(aliases=['movies', 'filme', 'filmes'], help='Download Movies. You can send multiple links.')
async def movie(ctx, *links):
    folder = os.getenv('FOLDER_MOVIES')
    await download(ctx, folder, *links)


@bot.command(aliases=['remova', 'remover'], help="Remove torrent. Need to pass the torrent ID")
async def remove(ctx, id=None):
    if not id:
        return await ctx.send('You must send an id.' + get_emoji('bad'))

    try:
        subprocess.run(['transmission-remote', '-t', id, '-r'], capture_output=True, check=True)
    except subprocess.CalledProcessError:
        await ctx.send('Oops! I could not remove the torrent.' + get_emoji('bad'))
    else:
        await ctx.send('Removed!' + get_emoji('good'))


@bot.command(aliases=['clear', 'limpar'], help="Remove all concluded torrents.")
async def clean(ctx):
    try:
        torrents = get_torrents()
    except Exception:
        return await ctx.send('Sorry, an error occurred while processing the command.' + get_emoji('bad'))

    if not torrents:
        return await ctx.send('No torrents in the list!' + get_emoji('good'))

    command = []
    for torrent in torrents:
        if torrent.completed():
            command += ['-t', torrent.id, '-r']

    if not command:
        return await ctx.send('No completed torrents in the list!' + get_emoji('good'))

    try:
        subprocess.run(['transmission-remote'] + command, check=True)
    except subprocess.CalledProcessError:
        await ctx.send('Oops! I could not remove the torrents.' + get_emoji('bad'))
    else:
        await ctx.send('All clean now! :smiling_face_with_tear:')


# Run the bot
bot.run(TOKEN)
