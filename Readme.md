# Flask Video Streaming API

This is a Flask API for streaming video and controlling playback using endpoints.

## Installation

1. Clone the repository:

```bash

   git clone https://github.com/kpndevroot/flaskapi.git

```

2. Navigate to the project directory:

```bash
   cd flaskapi
```

3. Create a virtual environment:

```bash
   python -m venv venv
```

4. Activate the virtual environment:

   - On Windows:

```bash
     venv\Scripts\activate
```

- On macOS/Linux:

```bash
     source venv/bin/activate
```

5. Install the required dependencies:

```bash
   pip install -r requirements.txt
```

## Running the Application

To run the Flask application using Gunicorn, use the following command:

```bash
gunicorn -w 1 -b 0.0.0.0:5000 main:app

```

Replace `localhost:5000` with the path to your project directory.

development server

```bash
   gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Press CTRL+C to stop the application. Next, deactivate from the Python virtual environment with the following command:

```bash
   deactivate
```

Create a Systemd Service File for Flask Application

```bash
   nano /etc/systemd/system/flask.service
```

Add the following lines:

```bash
[Unit]
Description=Gunicorn instance to serve Flask
After=network.target
[Service]
User=root
Group=www-data
WorkingDirectory=/home/rpi/flaskapi
Environment="PATH=/home/rpi/flaskapi/api/bin"
ExecStart=/home/rpi/flaskapi/api/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app
[Install]
WantedBy=multi-user.target

```

set proper ownership and permission to flask project:

```bash
chown -R root:www-data /home/rpi/flaskapi &&
chmod -R 775 /root/project
```

Reload the systemd daemon

```bash
   systemctl daemon-reload
```

start the flask service and enable it to start at system reboot:

```bash
systemctl start flask && systemctl enable flask

```

verify the status of the flask

```bash
   systemctl status flask

```

## API Endpoints

- **GET /hello**: Returns a "Hello World" message.

- **GET /play**: Starts playing the video.

- **GET /pause**: Pauses the video playback.

- **GET /stream_video**: Streams the video content.

Ensure that VLC is installed on your system for video playback to work properly.
