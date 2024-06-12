from flask import Flask, jsonify, request
from pyngrok import ngrok
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import vlc
app = Flask(__name__)


video_files = {
    "video1": "video1.mp4",
    "video2": "video2.mp4",

}

media_player = None

ngrok.set_auth_token("2fbK3XRIsUtUAbECqw6NoKbLE0K_sL6ikr327mkm7NZBmAod")
def initialize_player(video_file):
    global media_player
    if media_player is not None:
        media_player.stop()
    media = vlc.Media(video_file)
    media_player = vlc.MediaPlayer()
    media_player.set_media(media)
    media_player.set_fullscreen(True)
    media_player.play()


# Initialize Firebase Admin SDK
cred = credentials.Certificate("credential.json")  # Replace with your service account key
firebase_admin.initialize_app(cred)

db = firestore.client()

def create_ngrok_tunnel(port):
    try:
        # Open a TCP tunnel on the specified port
        tunnel = ngrok.connect(port, "tcp")
        tunnel_url = tunnel.public_url

        print("Ngrok tunnel created successfully.")
        print("Tunnel URL:", tunnel_url)

        # Check if there are any existing documents in the collection
        tunnel_ref = db.collection('ngrok_tunnels')
        existing_docs = tunnel_ref.get()

        # If there are existing documents, update the first one found with the current tunnel URL
        if existing_docs:
            for doc in existing_docs:
                doc_ref = tunnel_ref.document(doc.id)
                doc_ref.update({'tunnel_url': tunnel_url})
                print("Existing tunnel URL updated in Firebase.")
                break  # Update only the first document found

        # If there are no existing documents, create a new one with the current tunnel URL
        else:
            tunnel_ref.add({'tunnel_url': tunnel_url})
            print("New tunnel URL stored in Firebase.")

    except Exception as e:
        print("Error creating ngrok tunnel:", e)


@app.route('/hello', methods=['GET'])
def helloworld():
    print('Hello')
    data = {"data": "Hello World"}
    return jsonify(data)

@app.route('/play/<video_name>', methods=['GET'])
def play(video_name):
    print('Play')
    video_file = video_files.get(video_name)
    if video_file:
        initialize_player(video_file)
        data = {"data": f"Playing {video_name}"}
    else:
        data = {"error": "Video not found"}
    return jsonify(data)


@app.route('/pause', methods=['GET'])
def pause():
    print('Pause')
    if media_player is not None:
        media_player.pause()
    data = {"data": "Paused"}
    return jsonify(data)
@app.route('/p', methods=['GET'])
def plays():
    print('Play')
    if request.method == 'GET':
        if media_player is None:
            initialize_player()
        media_player.play()
        data = {"data": "Playing"}
        return jsonify(data)


if __name__ == "__main__":
    port = 5000  # Change to the port your Flask app runs on
    create_ngrok_tunnel(port)
    app.run(debug=True)
