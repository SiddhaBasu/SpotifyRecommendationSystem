from flask import Flask, request, url_for, session, redirect, render_template
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import math

CLIENT_ID = "50e136d283084eada48025c49238bce2"
CLIENT_SECRET = "blahblahblah"
TOKEN_INFO = "token_info"

permissions = ["user-library-read", "user-top-read", "playlist-read-private", "playlist-modify-private"]
alt_permissions = ["user-read-playback-state", "user-read-recently-played"]
permissions.extend(alt_permissions)
# app-remote-control for Spotify iOS and Android SDKs

app = Flask(__name__)

# IDEAS
# ---- based off user's last 50 liked songs, develop a playlist of songs they may like
# ---- based off of a user's most played playlist, add songs that they do not know or have not played ever


# questions
# ---- how do you determine that a user does not know a song? if it's not in any playlist, ideally with low streaming counts

"""
current_user_saved_tracks_contains(tracks=None)
Check if one or more tracks is already saved in the current Spotify user’s “Your Music” library.

Parameters:
tracks - a list of track URIs, URLs or IDs

playlist_items(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track', 'episode'))
Get full details of the tracks and episodes of a playlist.

Parameters:
playlist_id - the playlist ID, URI or URL
fields - which fields to return
limit - the maximum number of tracks to return
offset - the index of the first track to return
market - an ISO 3166-1 alpha-2 country code.

additional_types - list of item types to return.
valid types are: track and episode

playlist_tracks(playlist_id, fields=None, limit=100, offset=0, market=None, additional_types=('track',))
Get full details of the tracks of a playlist.

Parameters:
playlist_id - the playlist ID, URI or URL
fields - which fields to return
limit - the maximum number of tracks to return
offset - the index of the first track to return
market - an ISO 3166-1 alpha-2 country code.

additional_types - list of item types to return.
valid types are: track and episode
"""


app.secret_key = "fjkjsdfhjksh"
app.config['SESSION_COOKIE_NAME'] = "SID B COOKIE"

@app.route('/')
def login():
    sp_oauth = createSpotifyOAuth()
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirectPage(): # request parameters may be given here in other frameworks
    sp_oauth = createSpotifyOAuth()
    session.clear()
    code = request.args.get('code') # trading access code for access token
    token_info = sp_oauth.get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for("getTracks", _external=True)) # _external=True means it'll create the absolute path

def getRecentlyPlayedTracks(sp):
    recentlyPlayedString = ""
    recentlyPlayed = sp.current_user_recently_played(limit=50)["items"]

    for song in recentlyPlayed:
        song = song['track']
        artists = [artist['name'] for artist in song['artists']]
        recentlyPlayedString += f"{song['name']} by {', '.join(artists[:-1]) + ' & ' +  artists[-1] if len(song['artists']) > 1 else artists[0]} <br>"

def getTopTracks(sp):
    topTracksString = ""
    for i in range(10):
        topTracks = sp.current_user_top_tracks(limit=50, offset=(50*i))["items"]

        for song in topTracks:
            artists = [artist['name'] for artist in song['artists']]
            topTracksString += f"{song['name']} by {', '.join(artists[:-1]) + ' & ' +  artists[-1] if len(song['artists']) > 1 else artists[0]} <br>"
        

@app.route('/getTracks')
def getTracks():
    try:
        token_info = get_token()
    except:
        print("User not logged in")
        return redirect("/") # to log in page

    sp = spotipy.Spotify(auth=token_info['access_token'])

    artistIDs = {}
    #if key in dic.keys():

    genreStrengths = {}


    for i in range(10):
        topTracks = sp.current_user_top_tracks(limit=50, offset=(50*i))["items"]
        genreWeight = math.exp(-i/4)

        for song in topTracks:
            artistID = song['artists'][0]['id']
            
            if artistID not in artistIDs.keys():
                artistData = sp.artist(artistID)
                artistIDs[artistID] = artistData['genres']
            
            for genre in artistIDs[artistID]:
                if genre in genreStrengths.keys():
                    genreStrengths[genre] += genreWeight * 10
                else:
                    genreStrengths[genre] = genreWeight * 10
            
    genreStrengths = dict(sorted(genreStrengths.items(), key=lambda item: item[1], reverse=True))
    genreStrengths = dict(list(genreStrengths.items()))[0:8]

    labels = []
    values = []
    colors = ["#003f5c","#2f4b7c","#665191","#a05195","#d45087","#f95d6a","#ff7c43","#ffa600"]

    for key, value in genreStrengths.items():
        labels.append(key)
        values.append(value)

    return render_template('chart.html', set=zip(values, labels, colors))

def get_token():
    # make sure token didn't expire
    # and if there is token data still
    token_info = session.get(TOKEN_INFO, None)
    if not token_info:
        raise "Exception"
    now = int(time.time())

    is_expired = token_info['expires_at'] - now < 60 # close to being expired
    if is_expired:
        sp_oauth = createSpotifyOAuth()
        token_info = sp_oauth.refresh_access_token(token_info["refresh_token"])
    return token_info

def createSpotifyOAuth():
    return SpotifyOAuth(
        client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        redirect_uri=url_for('redirectPage', _external=True), # url_for replaces http://localhost and makes deployment urls easy
        scope=" ".join(permissions))
