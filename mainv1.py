from flask import Flask, jsonify, request
import vlc

app = Flask(__name__)

video_files = {
    "video1": "video1.mp4",
    "video2": "video2.mp4",

}

media_player = None

def initialize_player(video_file):
    global media_player
    if media_player is not None:
        media_player.stop()
    media = vlc.Media(video_file)
    media_player = vlc.MediaPlayer()
    media_player.set_media(media)
    media_player.play()

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

if __name__ == '__main__':
    app.run(debug=True)
