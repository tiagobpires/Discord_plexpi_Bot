import subprocess
from models import Torrent


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
