import time
from pathlib import Path
from typing import Union

import tqdm
from fire import Fire
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from src.get_gdrive_service import Resource, get_gdrive_service


def download_file(
    file_id: str,
    service: Resource,
    dst_fpath: Union[str, Path] = None,
):
    try:
        # pylint: disable=maybe-no-member
        request = service.files().get_media(fileId=file_id)

        if dst_fpath is None:
            dst_fpath = (
                service.files()
                .get(fileId=file_id, supportsAllDrives=True)
                .execute()["name"]
            )

        time_1 = time.time()
        with tqdm.tqdm(
            smoothing=True,
            desc=f"Download to {dst_fpath}",
            unit="%",
        ) as pbar:
            with open(dst_fpath, "wb") as file:
                downloader = MediaIoBaseDownload(file, request)
                done = False
                while done is False:
                    status, done = downloader.next_chunk()
                    if status:
                        time_2 = time.time()
                        progress = status.progress() * 100
                        current_progress = progress - pbar.n
                        current_speed = (
                            current_progress * status.total_size / (time_2 - time_1)
                        )
                        current_speed /= 1024 * 1024 * 100
                        pbar.update(round(current_progress, 2))
                        pbar.set_postfix_str(f"Speed: {current_speed:.2f} MB/s")
                        time_1 = time_2
        return True

    except HttpError as error:
        print(f"An error occurred: {error}")
        print(f"Failed to download {file_id}")
        return False


def main(
    file_id: str,
    dst_path: str = None,
    credentials_file: str = "credentials.json",
):
    with get_gdrive_service(credentials_file) as service:
        download_file(file_id, service, dst_path)


if __name__ == "__main__":
    Fire(main)
