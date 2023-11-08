# Deezer2Spotify.humanWasHere

## Table of matters
1. [General informations](#deezer2spotify_script-)
2. [Features](#features--eyes)
3. [Services](#services-apis)
4. [Informations to provide](informations2enter-)
5. [Installation](#installation-)
6. [Modules](#modules-)
<!--7. [Warning](#warning-)-->

## deezer2spotify_script :

deezer2spotify is a tool I developped in Python in order to transfert songs from a Deezer playlist to a new Spotify one.
You only have to enter a few different information in order to automatically run the script.
It is not very visual but very practical !

### Features : :eyes:

* gets token from Deezer and Spotify
* gets data from the given Deezer playlist
* finds corresponding songs in the Spotify database
* gets the URIs of these songs
* for each tracks, checks for duplicate (already in destination playlist) and gets id, artist name and title of the song
* finally, adds track or doesn't !


## Services (APIs):

| Service | Link | Description
| :--- | :--- | :---
| Deezer | [https://developers.deezer.com/myapps](https://developers.deezer.com/myapps) | Get your Deezer app access token here !
| Spotify | [https://developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) | Get your Spotify app access token here !


## Informations2enter :
To use the script, you will need to enter the following informations at the script's launch :
* Deezer access token (you can find it in your Deezer app settings using the Deezer API)
* Deezer playlist ID (you can find it in your Deezer playlist settings)
* Spotify client ID (you can find it in your Spotify app settings using the Spotify API)
* Spotify client secret (you can find it in your Spotify app settings using the Spotify API)
* Spotify user ID (I sadly can't remember where I got it... sorry for your time !)
* Spotify playlist ID (you can find it in your Spotify playlist settings)


## Installation :
Create a folder on your local machine. In cmd : 
```
cd <your_folder_name>
```
```
git clone https://github.com/humanWasHere/deezer2spotify_user
```
Download the libraries used in the script
```
pip install -r requirements.txt
```
Then run deezer2spotify.py with the command 
```
python deezer2spotify.py
```
or
```
python3 deezer2spotify.py
```
You will have to follow the instructions and let the script do its thing !


### Modules :
Here is a list of all the modules I have used :

* base64 - Version bs4==0.0.1
* requests - Version requests==2.31.0
* urlencode from urllib.parse - Version urllib3==1.26.12
* webbrowser - Version ?
* time - Version ?
* pyautogui - Version PyAutoGUI==0.9.53
* pyperclip - Version pyperclip==1.8.2

<!--### Warning
Apparently, deleting a Spotify playlist as a user doesn't delets everything -> tracks can still have their status present in the playlist-->
