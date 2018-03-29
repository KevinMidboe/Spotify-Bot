import pprint
import sys
import spotipy
import os
import spotipy.util as util

def getKeysAndPlaylist():

    clientID = '9f8caa1d3bb44187854c5282f94f83b2'
    clientSecret = os.environ.get('client_secret')
    print("HHEHEHEHEHE")
    print(clientSecret)
    redirectUri = 'https://blooming-refuge-48604.herokuapp.com/'
    playlistID = 'https://open.spotify.com/user/ribe1912/playlist/0mTtRpipjSnsq3Rgd12CQu'

    return clientID, clientSecret, redirectUri, playlistID

def getUsernameAndLinks():
    if len(sys.argv) > 2:
        username = sys.argv[1]
        trackLinks = sys.argv[2:]
    else:
        print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
        sys.exit()
    return username, trackLinks

def checkAndConvertLink(trackLinks):
    linkString = trackLinks[0]
    #'?' + str is added to the hyperlink when copying songs from the app / desktop. Remove this to run in webbrowser
    questionMarkIndex = linkString.find('?')
    if questionMarkIndex != -1:
        trackLinks = [linkString[0:questionMarkIndex]] #Only supports adding one song at a time so far.

    else:
        pass
    return trackLinks

def addSongToPlaylist():

    #Get keys which allows to connect to the Spotify app
    clientID, clientSecret, redirectUri, playlistID = getKeysAndPlaylist()
    username, trackLinks = getUsernameAndLinks()
    trackLink = checkAndConvertLink(trackLinks)

    #This gets the authentication needed to add song to the user's playlist
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id=clientID, client_secret=clientSecret, redirect_uri = redirectUri)
    if token:
        sp = spotipy.Spotify(token)
        sp.trace = False
        sp.trace_out = False

        #Append to spotify playlist
        results = sp.user_playlist_add_tracks(username, playlistID, trackLinks)
        print(results)
    else:
        print("Can't get token for", username)

if __name__ == '__main__':
    addSongToPlaylist()
