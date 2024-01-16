from PIL import Image
from PIL import ImageOps
from collections import defaultdict
import numpy as np
import pytesseract
import cv2
import requests

import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = 'a8311e104480459b903a013a5dc01610'
SPOTIPY_CLIENT_SECRET = '521e0fae310c4fd4b7e470f3f3f7f9e6'
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:8080'



words = defaultdict(list)
song_list = defaultdict(list)
name = ""
public = False
username = "31f4ptezt4qmjrbw36lbjqsmq4su"


def process_image():
    # pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    filename = 'image.jpeg'
    im = Image.open(filename)
    im = ImageOps.invert(im)
    im = ImageOps.autocontrast(im)
    im = ImageOps.grayscale(im)
    im.save('proccessed_image.jpeg')
    image = cv2.imread('proccessed_image.jpeg')
    results = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    return results

def filter_image_results(results):
    for i in range(0, len(results["text"])):
        if results["text"][i] != '' and results["text"][i] != " " and results["text"][i] != ".":
            words["text"].append(results["text"][i])
            words["left"].append(results["left"][i])
            words["top"].append(results["top"][i])
            words["block_num"].append(results["block_num"][i])
            words["line_num"].append(results["line_num"][i])
            words["conf"].append(results["conf"][i])
    pass

def organize_image_data():
    string = ""
    title = 0
    x_coord = words["left"][0] - 1

    for i in range(0, len(words["text"])):
        if words["left"][i] in (x_coord, x_coord + 1, x_coord + 2):
            if title == 1:
                song_list["title"].append(string)
                string = words["text"][i]
                title = 0
            else:
                if i != 0:
                    song_list["artist"].append(string)
                string = words["text"][i]
                title = 1
        else:
            string = string + " " + words["text"][i]
    song_list["artist"].append(string)
    for i in range(0, len(song_list["title"])):
        print("pos:", i, "name:", song_list["title"][i], " artists:", song_list["artist"][i])
    pass

def user_correct_data():
    user_input = input("Is a word wrong? (Y/N) ")
    sem = 0
    if user_input == "Y":
        sem = 1
    while sem == 1:
        user_input = input("On what position? ")
        if int(user_input) < 0 or int(user_input) >= len(song_list["title"]):
            print("Please give a valid position.")
        else:
            i = int(user_input)
            user_input = input("Is the title or the artist wrong? (T/A) ")
            if user_input == "T":
                user_input = input("Please give the correct title: ")
                song_list["title"][i] = user_input
            elif user_input == "A":
                user_input = input("Please give the correct artist: ")
                song_list["artist"][i] = user_input
            else:
                print("Please give a valid response.")
        
        for i in range(0, len(song_list["title"])):
            print("pos:", i, "name:", song_list["title"][i], " artists:", song_list["artist"][i])

        user_input = input("Is anything else wrong? (Y/N) ")
        sem = 0
        if user_input == "Y":
            sem = 1
    pass
    
def spotify_user_input():
    name = input("What would you like to be the name of the Playlist? ")
    user_input = input("Would you like the playlist to be Public or Private? (T/F) ")
    public = False
    if user_input == "T":
        public = True
    return name, public

def spotify_create_playlist(name, public):
    scope = "playlist-modify-public,playlist-modify-private"
    public = True
    token = SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope,
        username=username
        )
    sp = spotipy.Spotify(auth_manager = token)
    sp.user_playlist_create(user=username, name=name, public=public)
    playlist_id = sp.user_playlists(user=username)
    playlist = playlist_id['items'][0]['id']
    list_of_songs = []
    for i in range(0, len(song_list["title"])):
        sem = 0
        result = sp.search(q=song_list["title"][i])
        for j in range(0, len(result['tracks']['items'])):
            artists = result['tracks']['items'][j]['artists']
            for k in range(0, len(artists)):
                if artists[k]['name'] in song_list["artist"][i].split(','):
                    list_of_songs.append(result['tracks']['items'][j]['uri'])
                    sem = 1
                    break
            if sem == 1:
                break
    sp.user_playlist_add_tracks(user=username, playlist_id=playlist, tracks=list_of_songs)

    pass

def spotify():
    name, public = spotify_user_input()
    spotify_create_playlist(name, public)
    pass

ret = process_image()
filter_image_results(results=ret)
organize_image_data()
user_correct_data()
spotify()