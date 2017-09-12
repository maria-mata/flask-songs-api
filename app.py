# ----- IMPORTS -----
import sqlite3, json
from flask import Flask, request, jsonify

app = Flask(__name__)

# ----- ROUTES -----
# GET, POST to list
@app.route('/api/songs', methods=['GET', 'POST'])
def collection():
    if request.method == 'GET':
        all_songs = get_all_songs()
        return json.dumps(all_songs)
    elif request.method == 'POST':
        data = request.form
        result = add_song(data['artist'], data['title'], data['rating'])
        return jsonify(result)

# GET, PUT, DELETE (by ID)
@app.route('/api/songs/<song_id>', methods=['GET', 'PUT', 'DELETE'])
def resource(song_id):
    if request.method == 'GET':
        song = get_single_song(song_id)
        return json.dumps(song)
    elif request.method == 'PUT':
        pass # handle PUT song by ID
    elif request.method == 'DELETE':
        pass # handle DELETE request

# Helper functions
def add_song(artist, title, rating):
    try:
        with sqlite3.connect('songs.db') as connection:
            cursor = connection.cursor()
            cursor.execute("""INSERT INTO songs (artist, title, rating)
                values (?, ?, ?);""", (artist, title, rating,))
            result = {'status': 1, 'message': 'Song added'}
    except:
        result = {'status': 0, 'message': 'Error'}
    return result

def get_all_songs():
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM songs ORDER BY id desc")
        all_songs = cursor.fetchall()
        return all_songs

def get_single_song(song_id):
    with sqlite3.connect('songs.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM songs WHERE id = ?", (song_id,))
        song = cursor.fetchone()
        return song

# Below states that this source file is our main program
# Any files imported from other modules will have their name set to their module name
if __name__ == '__main__':
    app.debug = True
    app.run()
