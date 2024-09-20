from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import requests
from deep_translator import GoogleTranslator
import logging
import openai  # Add this import

logging.basicConfig(level=logging.DEBUG)

load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY')
if not openai.api_key:
    logging.error("OpenAI API key not found in environment variables.")

app = Flask(__name__)

MUSIXMATCH_API_KEY = os.getenv('MUSIXMATCH_API_KEY')
if not MUSIXMATCH_API_KEY:
    logging.error("Musixmatch API key not found in environment variables.")

def fetch_lyrics(song_name, artist_name):
    url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {
        'apikey': MUSIXMATCH_API_KEY,
        'q_track': song_name,
        'q_artist': artist_name,
        'format': 'json',
    }
    logging.debug(f"Requesting lyrics for song: {song_name} by artist: {artist_name}")
    response = requests.get(url, params=params)
    logging.debug(f"Musixmatch API URL: {response.url}")
    logging.debug(f"Response Status Code: {response.status_code}")
    data = response.json()
    logging.debug(f"Response Data: {data}")
    status_code = data['message']['header']['status_code']
    if status_code == 200:
        lyrics_body = data['message']['body']['lyrics']['lyrics_body']
        logging.debug("Lyrics fetched successfully.")
        return lyrics_body
    else:
        logging.error(f"Failed to fetch lyrics. API Status Code: {status_code}")
    return None

def translate_text(text, target_language='en'):
    translator = GoogleTranslator(source='auto', target=target_language)
    return translator.translate(text)

def enhance_translation(text):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can choose a different model if preferred
            prompt=f"Refine the following lyrics to make them more meaningful and contextually appropriate:\n\n{text}",
            temperature=0.7,
            max_tokens=1024,
        )
        enhanced_text = response.choices[0].text.strip()
        return enhanced_text
    except Exception as e:
        logging.error(f"OpenAI API error: {e}")
        return text  # Fallback to original if enhancement fails

def fetch_track_info(song_name, artist_name=''):
    url = "https://api.musixmatch.com/ws/1.1/track.search"
    params = {
        'apikey': MUSIXMATCH_API_KEY,
        'q_track': song_name,
        'q_artist': artist_name,
        'f_has_lyrics': 1,  # Filter tracks that have lyrics available
        's_track_rating': 'desc',  # Sort by track rating
        'format': 'json',
    }
    logging.debug(f"Searching for track: {song_name} by artist: {artist_name}")
    response = requests.get(url, params=params)
    logging.debug(f"Musixmatch API URL: {response.url}")
    logging.debug(f"Response Status Code: {response.status_code}")
    data = response.json()
    logging.debug(f"Response Data: {data}")

    status_code = data['message']['header']['status_code']
    if status_code == 200 and data['message']['body']['track_list']:
        track = data['message']['body']['track_list'][0]['track']
        logging.debug("Track found successfully.")
        return track
    else:
        logging.error(f"Failed to find track. API Status Code: {status_code}")
        return None

def fetch_artist_info(artist_id):
    url = "https://api.musixmatch.com/ws/1.1/artist.get"
    params = {
        'apikey': MUSIXMATCH_API_KEY,
        'artist_id': artist_id,
        'format': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['message']['header']['status_code'] == 200:
        artist = data['message']['body']['artist']
        logging.debug("Artist info fetched successfully.")
        return artist
    else:
        logging.error("Failed to fetch artist info.")
        return None

def fetch_album_info(album_id):
    url = "https://api.musixmatch.com/ws/1.1/album.get"
    params = {
        'apikey': MUSIXMATCH_API_KEY,
        'album_id': album_id,
        'format': 'json',
    }
    response = requests.get(url, params=params)
    data = response.json()
    if data['message']['header']['status_code'] == 200:
        album = data['message']['body']['album']
        logging.debug("Album info fetched successfully.")
        return album
    else:
        logging.error("Failed to fetch album info.")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    translated_lyrics = None
    original_lyrics = None
    error_message = None
    track_info = None
    artist_info = None
    album_info = None

    if request.method == 'POST':
        song_name = request.form.get('song_name')
        artist_name = request.form.get('artist_name', '')
        lyrics = request.form.get('lyrics')
        target_language = request.form.get('target_language', 'en')

        logging.debug(f"Received POST request with song_name: '{song_name}', artist_name: '{artist_name}', target_language: '{target_language}'")

        if song_name:
            track = fetch_track_info(song_name, artist_name)
            if track:
                track_info = track
                artist_info = fetch_artist_info(track['artist_id'])
                album_info = fetch_album_info(track['album_id'])
                # Fetch lyrics if available
                lyrics = fetch_lyrics(track['track_name'], track['artist_name'])
                if not lyrics:
                    error_message = "Lyrics not found for the song."
                    logging.error(error_message)
            else:
                error_message = "Track not found."
                logging.error(error_message)
        if lyrics:
            original_lyrics = lyrics  # Store the original lyrics
            try:
                translated_lyrics = translate_text(lyrics, target_language=target_language)
                logging.debug("Translation successful.")
                # Enhance the translated lyrics
                translated_lyrics = enhance_translation(translated_lyrics)
                logging.debug("Enhanced translation successful.")
            except Exception as e:
                error_message = "Translation failed. Please try again."
                logging.error(f"Translation error: {e}")
        elif not error_message:
            error_message = "Please provide a song name or lyrics."
            logging.error(error_message)

    return render_template(
        'index.html',
        translated_lyrics=translated_lyrics,
        original_lyrics=original_lyrics,
        error_message=error_message,
        track_info=track_info,
        artist_info=artist_info,
        album_info=album_info
    )

if __name__ == '__main__':
    app.run(debug=True)
