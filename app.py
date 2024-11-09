from flask import Flask, redirect, url_for, session, request, jsonify, render_template
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API credentials
SPOTIPY_CLIENT_ID = "5468d04e052d4d42b1cd08ee14956b4f"
SPOTIPY_CLIENT_SECRET = "dfcd68cab9384a93a213afb2a50ba972"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/callback"

# Configure Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                        client_secret=SPOTIPY_CLIENT_SECRET,
                        redirect_uri=SPOTIPY_REDIRECT_URI,
                        scope="user-read-recently-played")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('recent_tracks'))

@app.route('/recent_tracks')
def recent_tracks():
    token_info = session.get('token_info', None)
    if not token_info:
        return redirect(url_for('login'))

    sp = spotipy.Spotify(auth=token_info['access_token'])
    results = sp.current_user_recently_played(limit=10)
    tracks = [track['track']['name'] for track in results['items']]
    return jsonify(tracks)

@app.route('/mood', methods=['POST'])
def mood():
    user_mood = request.form['mood']
    # Placeholder for mood-based playlist and task recommendation
    return f"You entered: {user_mood}"

if __name__ == "__main__":
    app.run(debug=True)
