P2P - Picture to Playlist

Ciobanu George-Leonard
Atanasov Cosmina-Elena


This project uses a screenshot of a list of songs and it directly creates for you a playlist which you can add to your spotify account!

Using Optical Character Recognition software we have been able to successfully identify the words in the picture, and after using a sorting algorithm, we can identify all of the songs in the picture with 98% accuracy. After this proccess, a playlist is created, with the name of your choosing, which is made public or private, based on your decision. Immediately after you introduce your preferences, the songs from the image are directly added to said playlist, for you to listen to.

The project consists of 3 major steps:
    I.   Image Processing
    II.  Word Proccessing
    III. Spotify communication

I. Image Proccessing

The purpose of this step is to optimise the capabilities of the OCR algoritm (Optical Character Recognition).
Given that Spotify automatically uses a dark theme for its interface, the text on the application is white on black, which the OCR algorithm cannot understand or work with, so our first step becomes clear: turing the image into a negative of itself, thus turning the text to be black on a white background.
Since turning the image into a negative of itself causes some visual noise around the words, we have to clean that up with the famous openCV python library. Now we are finally ready to get the words from the image.


II. Word Proccessing

For the OCR algorithm we have chosen the pytesseract python library which is actually just a wrapper for Google's Tesseract-OCR Engine. Unfortunately, the Tesseract OCR only has a 98% accuracy, so some of the words might be wrong, but we figured, what better way to solve this problem than asking for the user's help. The user of the app can now correct any wrong words in the list of songs read from the picture.
To figure out what words make up part of the titles, and which make part of the artist we used the additional information received by the OCR algorithm. 
Firstly, we knew that the title always comes before the artist, so we could first read the words until we knew that we changed to the artists of the song. Given Spotify's format, we knew that the names of the artists of the song were displayed right under its title, so simply enough we read the words until we noticed that the x coordonate that we recieved was smaller that the earlier one, so then we can start reading the names of the artists. Also knowing that spotify displays the songs in a playlist one underneath the other, we simply had to apply the same algorithm again. So in summary, we know that we start with the title, so we read the title until the x coordonate becomes smaller, then we start reading the artists, and when that happens again, we know that we went on to the next song, and so on and so on.
In this way, we managed to sort the words we recieved by the OCR and store them in pairs. Now we are finally ready to move on to the next step.


III. Spotify communication

To be able to make modifications to a spotify account, we first had to open a Spotify developers account, and start an app. By doing that, we now received the right to ask for permissions from Spotify's Web-Api.
After being authorized, all we need to do now, is to communicate with the Spotify Web-Api to grant us the permission to modify playlists, which implicitly grants us the right to create a playlist, and so that's exactly what we'll do by using the spotipy python library that simplifies the interactions with Spotify's Web-API.
We first ask the user for the preffered name for the playlist, and if they wish for the playlist to be public or private.
After recieving the needed information from the user, we can now go ahead and create the playlist with the corresponding name and visibility. We should note that the newest playlist always recieves the smallest ID in the user's list of playlists. Knowing that, we can now go through the songs and add them one by one to the newly created playlist.

And just like that, we have now created a brand-new playlist with all of the songs that we screenshot from whatever friend's playlist.
