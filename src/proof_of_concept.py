#!/usr/bin/python2

__author__ = "Dan Seminara"

import gi
import dropbox
from gi.repository import Gst

def main():
    Gst.init()
    with open('.access_token') as f:
        access_token = f.read().strip()
    client = dropbox.client.DropboxClient(access_token)
    player = Gst.ElementFactory.make('playbin', 'player')
    path = raw_input('Please enter path to file to play in your Dropbox: ')
    music_file = client.media(path)
    
    player.set_property('uri', music_file['url'])
    player.set_state(Gst.State.PLAYING)

    raw_input('Press Enter to stop playing...')

if __name__ == '__main__':
    main()