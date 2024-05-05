from flask import Flask, Response, jsonify, request
import vlc

app = Flask(__name__)

media_file = "video.mp4"
media_player = None

def initialize_player():
    global media_player
    media = vlc.Media(media_file)
    media_player = vlc.MediaPlayer()
    media_player.set_media(media)
    media_player.play()  # Automatically play the video when initialized

# Call initialize_player() at the start to play the video automatically
initialize_player()

@app.route('/hello', methods=['GET'])
def helloworld():
    print('Hello')
    if request.method == 'GET':
        data = {"data": "Hello World"}
        return jsonify(data)

@app.route('/play', methods=['GET'])
def play():
    print('Play')
    if request.method == 'GET':
        if media_player is None:
            initialize_player()
        media_player.play()
        data = {"data": "Playing"}
        return jsonify(data)

@app.route('/pause', methods=['GET'])
def pause():
    print('Pause')
    if request.method == 'GET':
        if media_player is not None:
            media_player.set_pause(1)
            data = {"data": "Paused"}
            return jsonify(data)

@app.route('/stream_video')
def stream_video():
    def generate():
        if media_player is None:
            initialize_player()
        while True:
            frame = media_player.video_get_size(0)
            if frame:
                data = media_player.video_get_data(0)
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + data + b'\r\n'
            else:
                break
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
