

def step_upload(d, path):
    return 0

# import os
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload

# # Scopes required for uploading videos
# SCOPES = ['https://googleapis.com']

# def get_authenticated_service():
#     creds = None
#     # token.json stores the user's access and refresh tokens
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
#     # If there are no valid credentials available, let the user log in
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 'client_secret.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     return build('youtube', 'v3', credentials=creds)

# def upload_short(video_file_path, title, description, tags=[]):
#     youtube = get_authenticated_service()

#     # Append #Shorts to the title to ensure proper indexing
#     if "#shorts" not in title.lower():
#         title = f"{title} #Shorts"

#     body = {
#         'snippet': {
#             'title': title,
#             'description': description,
#             'tags': tags,
#             'categoryId': '22'  # 22 is for 'People & Blogs'
#         },
#         'status': {
#             'privacyStatus': 'public'  # Options: 'public', 'private', 'unlisted'
#         }
#     }

#     # Prepare video file chunk upload
#     media = MediaFileUpload(video_file_path, chunksize=-1, resumable=True, mimetype='video/mp4')

#     print(f"Uploading {video_file_path} to YouTube...")
#     request = youtube.videos().insert(
#         part=','.join(body.keys()),
#         body=body,
#         media_body=media
#     )

#     # Execute request and display final video ID
#     response = request.execute()
#     print(f"Success! Video uploaded. Video ID: {response.get('id')}")
#     print(f"Watch Link: https://www.youtube.com/shorts/{response.get('id')}")

# if __name__ == '__main__':
#     upload_short(
#         video_file_path='my_vertical_video.mp4',
#         title='My Awesome Python Automation Short',
#         description='This Short was automatically published via a custom Python script using the YouTube API v3.',
#         tags=['automation', 'python', 'shorts']
#     )
