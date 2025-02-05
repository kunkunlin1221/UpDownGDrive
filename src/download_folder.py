import datetime as dt
from pathlib import Path
from time import sleep

from fire import Fire

from src.download import download_file
from src.get_gdrive_service import get_gdrive_service


def main(
    folder_id: str,
    dst_folder: str,
    credentials_file: str = "credentials.json",
    scan_size: int = 1000,
):
    with get_gdrive_service(credentials_file) as service:
        results = (
            service.files()
            .list(
                q="'" + folder_id + "' in parents",
                pageSize=scan_size,
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        file_ids = results.get("files", [])
        file_ids = sorted(file_ids, key=lambda x: x["name"])
        dst_folder = Path(dst_folder)
        dst_folder.mkdir(parents=True, exist_ok=True)
        for file_dict in file_ids:
            file_id = file_dict["id"]
            dst_fpath = dst_folder / file_dict["name"]
            is_success = download_file(file_id, service, dst_fpath)
            if not is_success:
                current_time = dt.datetime.now()
                tomorrow = dt.datetime(
                    current_time.year, current_time.month, current_time.day + 1, 0, 0, 0
                )
                seconds_to_tomorrow = (
                    tomorrow.timestamp() - current_time.timestamp() + 1
                )
                print(
                    f"Exceed the download limitation (5T). Sleep for {seconds_to_tomorrow} seconds until tomorrow"
                )
                sleep(seconds_to_tomorrow)
                download_file(file_id, service, dst_fpath)


if __name__ == "__main__":
    Fire(main)
