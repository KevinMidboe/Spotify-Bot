# Creates a playlist for a user

import pprint
import sys
import os
import subprocess

import spotipy
import spotipy.util as util


if len(sys.argv) > 2:
    username = sys.argv[1]
    playlist_name = sys.argv[2]
    playlist_description = sys.argv[3]
else:
    print("Usage: %s username playlist-name playlist-description" % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id='9f8caa1d3bb44187854c5282f94f83b2',client_secret='fa0dd2c91ca045dbb53e158e49f1aa3d',redirect_uri='https://blooming-refuge-48604.herokuapp.com/')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    playlists = sp.user_playlist_create(username, playlist_name,
                                        playlist_description)
    pprint.pprint(playlists)
else:
    print("Can't get token for", username)
