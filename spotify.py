#!/usr/bin/env python3.6
import pprint
import sys
import spotipy
import os
import configparser
import spotipy.util as util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def getConfig():
    """
    Read path and get configuartion file with spotify settings
    :return: config settings read from 'config.ini'
    :rtype: configparser.ConfigParser
    """
    config = configparser.ConfigParser()
    config_dir = os.path.join(BASE_DIR, 'config.ini')
    config.read(config_dir)

    config_values = list(dict(config.items('Spotify')).values())
    if any(value.startswith('YOUR') for value in config_values):
        print('Please set variables in config.ini file.')
        exit(0)

    return config

def getLinks():
    if len(sys.argv) > 1:
        trackLinks = sys.argv[1:]
    else:
        print("Usage: %s  track_id ..." % (sys.argv[0],))
        sys.exit()

    return trackLinks

def checkAndConvertLink(trackLinks):
    linkString = trackLinks[0]
    #Just getting the base-62 number out of the spotify link so that links from browser, desktop and app can be used
    trackStringIndex = linkString.find('track/')
    questionMarkIndex = linkString.find('?')
    print(trackStringIndex)
    print(questionMarkIndex)
    if questionMarkIndex != -1:
        print("Getting the base-62 numbers out of hyperlink")
        trackLinks = [linkString[trackStringIndex + len('track/'): questionMarkIndex]] #Only supports adding one song at a time so far.

    else:
        print("Link format is already in base-62 form")
        pass

    return trackLinks

def addSongToPlaylist():
    config = getConfig()
    trackLinks = getUsernameAndLinks()
    trackLinks = checkAndConvertLink(trackLinks)

    username = config['USERNAME']
    #This gets the authentication needed to add song to the user's playlist
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id=config['CLIENT_ID'], client_secret=config['CLIENT_SECRET'], redirect_uri = config['REDIRECT_URI'])
    if token:
        sp = spotipy.Spotify(token)
        sp.trace = False
        sp.trace_out = False

        #Append to spotify playlist
        results = sp.user_playlist_add_tracks(username, config['PLAYLIST_ID'], trackLinks)
        print(results)
    else:
        print("Can't get token for", username)

if __name__ == '__main__':
    addSongToPlaylist()
