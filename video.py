import os
from firebase_admin import storage, credentials, initialize_app

# Initialize Firebase Admin SDK
cred = credentials.Certificate("./credential.json")
firebase_app = initialize_app(cred,{
    'storageBucket': 'pdcdb-ed421.appspot.com'
})

# Initialize Firebase Storage
storage_client = storage.bucket(app=firebase_app)

# Specify the folder in Firebase Storage containing the videos
folder_name = "videos"

local_directory = "./"

# Ensure local directory exists
os.makedirs(local_directory, exist_ok=True)

# Retrieve list of blobs (files) in the specified folder
blobs = storage_client.list_blobs(prefix=folder_name)

# Download each video file
for blob in blobs:
    # Extract the file name from the blob path
    filename = os.path.basename(blob.name)
    
    # Download the video file to local storage
    blob.download_to_filename(os.path.join(local_directory, filename))
    
    print(f"Downloaded {filename}")

print("All videos downloaded successfully.")




