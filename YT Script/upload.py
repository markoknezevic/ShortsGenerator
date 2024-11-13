from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account
from datetime import datetime, timedelta


import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scope for YouTube upload permissions
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate_youtube():
    creds = None
    # Check if token.json already exists; it stores the user's access and refresh tokens
    if os.path.exists('auth/token.json'):
        creds = Credentials.from_authorized_user_file('auth/token.json', SCOPES)

    # If credentials are invalid or do not exist, initiate the OAuth flow
    if not creds or not creds.valid:
        # Refresh token if expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # If no token or unable to refresh, start OAuth flow for new credentials
            flow = InstalledAppFlow.from_client_secrets_file('auth/yu.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials to token.json for future access
        with open('auth/token.json', 'w') as token_file:
            token_file.write(creds.to_json())

    return creds

# Authenticate and get credentials
creds = authenticate_youtube()

youtube = build('youtube', 'v3', credentials=creds)
i = 4

with open(f'content/title_text_{i}.txt', 'r') as file:
    # Read the content of the file
    title_text = file.read()
 
with open(f'general_description.txt', 'r') as file:
    # Read the content of the file
    general_description = file.read()


# Define video metadata
body = {
    'snippet': {
        'title': title_text,
        'description': general_description,
        'tags': ['shorts'],
        'categoryId': '24'
    },
    'status': {
        'privacyStatus': 'private',  # Keep it private until publish time
    }
}

# Upload video
media = MediaFileUpload(f'final_video/final_video_{i}.mp4', chunksize=-1, resumable=True)
request = youtube.videos().insert(part='snippet,status', body=body, media_body=media)
response = request.execute()

print(f"Scheduled video uploaded. Video ID: {response['id']}")
