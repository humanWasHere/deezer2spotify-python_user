### code automation playlist transfert deezer2spotify
# import base64
import requests
# import json
from urllib.parse import urlencode
# # modules to automate the authentification process
import webbrowser
import time
import pyautogui
import pyperclip

# get access token
def get_access_token(spotify_client_id, spotify_client_secret):
    # Authorization Endpoint URL
    authorization_url = 'https://accounts.spotify.com/authorize'
    # Redirect URI
    redirect_uri = 'https://www.google.com/'
    # permissions of the token - Add additional scopes as needed
    scopes = ['playlist-modify-private', 'playlist-read-private']

    # Generate the authorization URL
    params = {
        'client_id': spotify_client_id,
        'response_type': 'code',
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes)
    }
    authorization_url = authorization_url + '?' + urlencode(params)

    # Open the authorization URL in a web browser
    webbrowser.open(authorization_url)
    # Wait for the page to load
    time.sleep(3)
    # Move the mouse to the address bar
    pyautogui.hotkey('ctrl', 'l')
    # Copy the URL from the address bar
    pyautogui.hotkey('ctrl', 'c')
    # Get the content of the clipboard
    clipboard_content = pyperclip.paste()
    # Print the clipboard content
    # print(clipboard_content)

    # close last opened tab 
    # import keyboard 
    # keyboard.press_and_release('ctrl+w') # closes the last tab

    # Once you have the authorization code, exchange it for an access token
    token_url = 'https://accounts.spotify.com/api/token'
    
    code = clipboard_content.split("code=",1)[1]

    # Request access token
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri,
        'client_id': spotify_client_id,
        'client_secret': spotify_client_secret
    }
    response = requests.post(token_url, data=data)

    # Get the access token and other response data
    if response.status_code == 200:
        print("Authentification succeded !")
        response_data = response.json()
        spotify_access_token = response_data['access_token']
        refresh_token = response_data['refresh_token']
        expires_in = response_data['expires_in']
        return spotify_access_token
    else:
        print("Failed to retrieve access token:", response.text, "\ninvalid authentification - end of the program")


# Deezer credentials
deezer_access_token = ""
deezer_playlist_id = ""

# Spotify credentials
spotify_client_id = ""
spotify_client_secret = ""
spotify_user_id = ""
spotify_playlist_id = ""



# function to get track info from Deezer API
def get_deezer_track_info(track_id):
    url = "https://api.deezer.com/track/" + str(track_id)
    headers = {"Authorization": "Bearer " + deezer_access_token}
    response = requests.get(url, headers=headers)
    return response.json()

notFoundTracks = []
# function to get track info from Spotify API
def get_spotify_track_info(track_name, artist_name, access_token):
    url = f"https://api.spotify.com/v1/search?q=track:{track_name}%20artist:{artist_name}&type=track"
    headers = {
        "Authorization": "Bearer " + spotify_access_token
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get("tracks", {}).get("items", [])
        if tracks:
            return tracks[0]["uri"]
        else:
            print("No matching track found for " + track_name + " by " + artist_name + ".")
            notFoundTracks.append(track_name + " from " + artist_name)
    else:
        print("Failed to retrieve track info:", response.text)

# This function gets all the uris of the songs in the playlist
all_uris = []
def get_playlist_track_uris(playlist_id, access_token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    params = {
        "limit": 100,
        "offset": 0
    }

    while url:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            tracks = data.get('items', [])
            for track in tracks:
                uri = track['track']['uri']
                all_uris.append(uri)
            total = data['total']
            offset = params['offset'] + params['limit']
            if offset < total:
                params['offset'] = offset
            else:
                break
        else:
            print("Failed to retrieve playlist tracks:", response.text)
            return []
    # return all_uris

# Function to add track to Spotify playlist
def check_duplicate_and_add_track(playlist_id, track_uri, access_token, title_info, artist_info):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    headers = {
        "Authorization": "Bearer " + access_token,
        "Content-Type": "application/json"
    }
    params = {
        "ids": track_uri
    }
    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        tracks = data.get('tracks', [])
        # we check for duplicates here
        if track_uri in all_uris:
            print("Song '" + title_info + "' from '" + artist_info + "' is already in the playlist.")
            pass
        else:
            # Add the track to the playlist
            data = {
                "uris": [track_uri]
            }
            response = requests.post(url, headers=headers, json=data)

            if response.status_code == 201:
                print("Track '" + title_info + "' from '" + artist_info + "' has been added to the playlist successfully!")
            # elif response.status_code == 400:
            #     print("Track '" + title_info + "' from '" + artist_info + "' was not find on Spotify.")
            else:
                print("Failed to add track '" + title_info + "' from '" + artist_info + "' to the playlist : \n", response.text)
    else:
        print("Failed to check if song is in playlist:", response.text)

def askStringNotEmpty2User(instructions):
    user_input = input(instructions)
    # while not user_input.isalpha():
    #     user_input = "Please enter a string : "
    # while user_input == "":
    #     user_input = input("Please enter something : ")
    return user_input

if __name__ == '__main__':
    deezer_access_token = askStringNotEmpty2User("Enter your Deezer access token (you can find it in your Deezer app settings using the Deezer API):\n")
    deezer_playlist_id = askStringNotEmpty2User('Enter your Deezer playlist ID (you can find it in your Deezer playlist settings):\n')
    spotify_client_id = askStringNotEmpty2User('Enter your Spotify client ID (you can find it in your Spotify app settings using the Spotify API):\n')
    spotify_client_secret = askStringNotEmpty2User('Enter your Spotify client secret (you can find it in your Spotify app settings using the Spotify API):\n')
    spotify_user_id = askStringNotEmpty2User('Enter your Spotify user ID (I can\'t remember where I got it...):\n')
    spotify_playlist_id = askStringNotEmpty2User('Enter your Spotify playlist ID (you can find it in your Spotify playlist settings):\n')
    # get Deezer playlist data
    url = "https://api.deezer.com/playlist/" + deezer_playlist_id
    headers = {"Authorization": "Bearer " + deezer_access_token}
    response = requests.get(url, headers=headers)
    playlist_data = response.json()
    # initializing the authentification and GET infos
    spotify_access_token = get_access_token(spotify_client_id, spotify_client_secret)
    get_playlist_track_uris(spotify_playlist_id, spotify_access_token)
    if len(all_uris) > 0:
        print("The playlist is already " + str(len(all_uris)) + " tracks long.\nHere is a dictionnary containing all the uris :\n", all_uris)
    # loop through Deezer tracks and add to Spotify playlist
    for track in playlist_data['tracks']['data']:
        deezer_track_info = get_deezer_track_info(track['id'])
        spotify_track_info = get_spotify_track_info(deezer_track_info['title'], deezer_track_info['artist']['name'], spotify_access_token)
        check_duplicate_and_add_track(spotify_playlist_id, spotify_track_info, spotify_access_token, deezer_track_info['title'], deezer_track_info['artist']['name'])
    if not notFoundTracks:
        print("All songs were found on Spotify !")
    else:
        print("\nThese " + str(len(notFoundTracks)) + "songs did not find any corresponding song on Spotify :\n", notFoundTracks)
        # deezer playlist number of tracks
        # deezerTrackCount = playlist_data.get('tracks', {}).get('total')
        deezerTrackCount = playlist_data.get('nb_tracks', 0)
        # we ask for the number of elements found || but warning here, we modify the array "all_uris", make sure you don't reuse it after in the code (helps for storage this way)
        # for element in notFoundTracks:
        #     print(element)
        #     # all_uris.remove(element)
        spotifyFound = len(all_uris)
        # otherLenght = int(deezerTrackCount) - len(notFoundTracks)
        if spotifyFound + len(notFoundTracks) == deezerTrackCount:
            # print(str(spotifyFound) + " or " + str(otherLenght) + " over " + str(deezerTrackCount) + " where found in Spotify")
            print(str(spotifyFound) + " over " + str(deezerTrackCount) + " where found in Spotify")

# get deezer playlist
# get track info

# search in spotify
# add spotify track in playlist

# to make it fully automated, ask user at the beginning of the program about his browser and his Deezer and Spotify API informations

# pip uninstall PyAutoGUI
# pip uninstall pyperclip
# the day I don't use it