import pprint
import sys
import spotipy
import os
import config as cnf
import spotipy.util as util


def getUsernameAndLinks():
    username = cnf.username
    if len(sys.argv) > 1:
        trackLinks = sys.argv[1:]
    else:
        print("Usage: %s  track_id ..." % (sys.argv[0],))
        sys.exit()

    return username, trackLinks

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

    username, trackLinks = getUsernameAndLinks()
    trackLinks = checkAndConvertLink(trackLinks)

    #This gets the authentication needed to add song to the user's playlist
    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username, scope, client_id=cnf.clientID, client_secret=cnf.clientSecret, redirect_uri = cnf.redirectUri)
    if token:
        sp = spotipy.Spotify(token)
        sp.trace = False
        sp.trace_out = False

        #Append to spotify playlist
        results = sp.user_playlist_add_tracks(cnf.username, cnf.playlistID, trackLinks)
        print(results)
    else:
        print("Can't get token for", username)

if __name__ == '__main__':
    addSongToPlaylist()
