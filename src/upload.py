import time
from pathlib import Path
from typing import Union

import tqdm
from fire import Fire
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

from src.get_gdrive_service import Resource, get_gdrive_service


def upload_file(
    file_path: Union[str, Path],
    folder_id: str,
    service: Resource,
):
    folders = [folder_id]
    file_path = Path(file_path)

    file_metadata = {
        "name": file_path.name,
        "parents": folders,
    }
    media = MediaFileUpload(file_path, chunksize=32 * 1024 * 1024, resumable=True)
    request = service.files().create(
        body=file_metadata, media_body=media, supportsAllDrives=True
    )
    try:
        with tqdm.tqdm(smoothing=True, desc=f"Upload {file_path}", unit="%") as pbar:
            time_1 = time.time()
            done = None
            while done is None:
                status, done = request.next_chunk()
                if status:
                    time_2 = time.time()
                    progress = status.progress() * 100
                    current_progress = progress - pbar.n
                    current_speed = (
                        current_progress * status.total_size / (time_2 - time_1)
                    )
                    current_speed /= 1024 * 1024 * 100
                    pbar.update(round(current_progress, 3))
                    pbar.set_postfix_str(f"Speed: {current_speed:.2f} MB/s")
                    time_1 = time_2
            request.execute()
            pbar.desc = f"Uploaded {file_path}"
        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Failed to upload {file_path}")
        return False


def main(
    file_path: str,
    folder_id: str,
    credentials_file: str = "credentials.json",
):
    with get_gdrive_service(credentials_file) as service:
        upload_file(file_path, folder_id, service)


if __name__ == "__main__":
    Fire(main)
