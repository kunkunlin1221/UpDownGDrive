from pathlib import Path
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from google_auth_oauthlib.flow import InstalledAppFlow
import fire
import tqdm
import os
import time

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          'https://www.googleapis.com/auth/drive.file']


def get_gdrive_service(credentials_file):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)


def get_file_size(file_path):
    return Path(file_path).stat().st_size


def upload_file(folder_id, credentials_file, file_path):
    folders = [folder_id]
    # service = get_gdrive_service()
    with get_gdrive_service(credentials_file) as service:
        file_path = Path(file_path)
        file_size = get_file_size(file_path)

        file_metadata = {
            "name": file_path.name,
            "parents": folders,
        }
        media = MediaFileUpload(
            file_path, chunksize=32*1024*1024, resumable=True)
        request = service.files().create(
            body=file_metadata, media_body=media, supportsAllDrives=True)
        response = None

        time_1 = time.time()
        try:
            with tqdm.tqdm(smoothing=True, desc=f'Upload {file_path}', unit='%') as pbar:
                while response is None:
                    status, response = request.next_chunk()
                    if status:
                        time_2 = time.time()
                        progress = status.progress()*100
                        current_progress = progress - pbar.n
                        current_speed = current_progress * status.total_size / (time_2 - time_1)
                        current_speed /= 1024 * 1024 * 100
                        pbar.update(round(current_progress, 3))
                        pbar.set_postfix_str(f"Speed: {current_speed:.2f} MB/s")
                        time_1 = time_2
                file = request.execute()
                print(f"File uploaded: {file.get('id')}")
            return True
        except Exception as e:
            print(f"Error: {e}")
            print(f"Failed to upload {file_path}")
            return False

    # service.close()

if __name__ == '__main__':
    fire.Fire(upload_file)
