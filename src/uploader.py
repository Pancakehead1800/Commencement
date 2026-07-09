import os
from pathlib import Path

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from constants import *

# YouTube upload scope
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


def get_authenticated_service():
    creds = None

    if os.path.exists(TOKENS_FILE):
        creds = Credentials.from_authorized_user_file(TOKENS_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SECRETS_FILE,
                SCOPES,
            )
            creds = flow.run_local_server(port=0)

        with open(TOKENS_FILE, "w") as f:
            f.write(creds.to_json())

    return build("youtube", "v3", credentials=creds)


def upload_short(video_path):
    youtube = get_authenticated_service()

    video_path = Path(video_path)

    # Use filename as title
    title = video_path.stem.replace("_", " ").replace("-", " ")

    if "#shorts" not in title.lower():
        title += " #Shorts"

    body = {
        "snippet": {
            "title": title,
            "description": "",
            "tags": ["shorts"],
            "categoryId": "24",
        },
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(
        str(video_path),
        mimetype="video/mp4",
        resumable=True,
    )

    print(f"Uploading {video_path.name}...")

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        _, response = request.next_chunk()

    video_id = response["id"]

    print("Upload complete!")
    print(f"Video ID: {video_id}")
    print(f"https://www.youtube.com/shorts/{video_id}")

    return video_id


def step_upload(path):
    return upload_short(path)


if __name__ == "__main__":
    pass