import datetime as dt
from pathlib import Path
from time import sleep

from fire import Fire

from src.get_gdrive_service import Resource, get_gdrive_service
from src.upload import HttpError, upload_file


def create_folder(service: Resource, folder_name: str, mother_folder_id: str = None):
    try:
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if mother_folder_id is not None:
            file_metadata["parents"] = [mother_folder_id]

        # pylint: disable=maybe-no-member
        file = service.files().create(body=file_metadata, fields="id", supportsAllDrives=True).execute()
        return file.get("id")

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def main(
    folder: str,
    mother_folder_id: str = None,
    credentials_file: str = "credentials.json",
):
    folder = Path(folder)
    file_paths = [x for x in sorted(folder.glob("*")) if x.is_file()]
    with get_gdrive_service(credentials_file) as service:
        folder_id = create_folder(service, folder.name, mother_folder_id)
        for file_path in file_paths:
            is_success = upload_file(file_path, folder_id, service)
            if not is_success:
                current_time = dt.datetime.now()
                tomorrow = dt.datetime(
                    current_time.year, current_time.month, current_time.day + 1, 0, 0, 0
                )
                seconds_to_tomorrow = (
                    tomorrow.timestamp() - current_time.timestamp() + 1
                )
                print(
                    f"Exceed the upload limitation (750GB). Sleep for {seconds_to_tomorrow} seconds until tomorrow"
                )
                sleep(seconds_to_tomorrow)
                upload_file(file_path, folder_id, service)


if __name__ == "__main__":
    Fire(main)
