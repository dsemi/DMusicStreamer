#!/usr/bin/python3

__author__ = "Dan Seminara"

import gi
import dropbox
import ujson as json
from gi.repository import Gst

# Python recipe for grabbing character
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt
    def __call__(self):
        import msvcrt
        return msvcrt.getch()
getch = _Getch()

# Takes a long time, limit to music folder to save time
def save_music_files(folder='/'):
    mfiles = []; files = client.metadata(folder)['contents']
    for f in files:
        if f['is_dir']:
            mfiles.extend(save_music_files(f['path']))
        elif f['mime_type'].startswith('audio'):
            mfiles.append(f['path'])
    return mfiles

def main():
    Gst.init()
    # Need to add actual authentication
    with open('.access_token') as f:
        access_token = f.read().strip()
    client = dropbox.client.DropboxClient(access_token)
    player = Gst.ElementFactory.make('playbin', 'player')

    # Browse files, not manually input path
    # This will mean remembering users, and the files in their Dropbox
    # Needs some kind of GUI or ncurses
    # Have some kind of manual rescan functionality
    path = input('Please enter path to file to play in your Dropbox: ')
    music_file = client.media(path)
    player.set_property('uri', music_file['url'])
    player.set_state(Gst.State.PLAYING)
    playing = 1
    while True:
        inp = getch()
        if inp == 'q':
            break
        elif inp == 'p':
            if playing:
                player.set_state(Gst.State.PAUSED)
            else:
                player.set_state(Gst.State.PLAYING)
            playing ^= 1


if __name__ == '__main__':
    main()