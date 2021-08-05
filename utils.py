import random
import subprocess
from models import Torrent


EMOJIS_ENABLE = True


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


def switch_emojis():
    global EMOJIS_ENABLE
    if EMOJIS_ENABLE:
        EMOJIS_ENABLE = False
        return 'Emojis turn off!'
    else:
        EMOJIS_ENABLE = True
        return 'Emojis turn on!' + get_emoji('good')


def get_emoji(type=None):
    if not EMOJIS_ENABLE:
        return ''

    good = [
        'grinning', 'smiley', 'smile', 'grin', 'laughing', 'relaxed', 'blush', 'innocent', 'slight_smile',
        'upside_down', 'relieved', 'smiling_face_with_3_hearts', 'kissing_heart', 'yum', 'stuck_out_tongue',
        'stuck_out_tongue_closed_eyes', 'stuck_out_tongue_winking_eye', 'sunglasses', 'nerd', 'star_struck',
        'partying_face', 'white_check_mark'
    ]

    bad = [
        'face_with_monocle', 'face_with_raised_eyebrow', 'slight_frown', 'confused', 'worried', 'pensive',
        'disappointed', 'frowning2', 'persevere', 'confounded', 'tired_face', 'weary', 'pleading_face', 'triumph',
        'face_exhaling', 'angry', 'cry', 'sob', 'flushed', 'fearful', 'cold_sweat', 'disappointed_relieved', 'sweat',
        'grimacing', 'hushed', 'frowning', 'anguished', 'open_mouth', 'neutral_face', 'face_with_spiral_eyes',
        'dizzy_face', 'woozy_face', 'thermometer_face', 'head_bandage'
    ]

    if type == 'good':
        emojis = good
    elif type == 'bad':
        emojis = bad
    else:
        emojis = good + bad

    return f' :{random.choice(emojis)}:'
