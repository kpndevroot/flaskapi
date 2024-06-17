#!/bin/bash

# Variables
USER="root"
GROUP="www-data"
WORKING_DIR="/home/rpi/flaskapi"
VENV_PATH="$WORKING_DIR/api/bin"
SERVICE_FILE="/etc/systemd/system/flask.service"

# Create a virtual environment and install Flask and Gunicorn if not already done
if [ ! -d "$VENV_PATH" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$WORKING_DIR/api"
    source "$VENV_PATH/activate"
    pip install Flask gunicorn
else
    echo "Virtual environment already exists."
fi

# Create the systemd service file
echo "Creating systemd service file..."
cat <<EOF > $SERVICE_FILE
[Unit]
Description=Gunicorn instance to serve Flask
After=network.target

[Service]
User=$USER
Group=$GROUP
WorkingDirectory=$WORKING_DIR
Environment="PATH=$VENV_PATH"
ExecStart=$VENV_PATH/gunicorn --bind 0.0.0.0:5000 wsgi:app

[Install]
WantedBy=multi-user.target
EOF

# Set proper ownership and permissions
echo "Setting ownership and permissions..."
chown -R $USER:$GROUP $WORKING_DIR
chmod -R 775 $WORKING_DIR

# Reload systemd daemon
echo "Reloading systemd daemon..."
systemctl daemon-reload

# Start and enable the flask service
echo "Starting and enabling flask service..."
systemctl start flask
systemctl enable flask

# Verify the status of the flask service
echo "Verifying flask service status..."
systemctl status flask
