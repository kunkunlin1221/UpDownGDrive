from pathlib import Path
import fire
from src.download import upload_file
import datetime as dt
from time import sleep


def main(credentials_file, folder_id, folder):
    files = [x for x in sorted(Path(folder).glob('*')) if x.is_file()]
    for file in files:
        is_success = upload_file(folder_id, credentials_file, file)
        if not is_success:
            current_time = dt.datetime.now()
            tomorrow = dt.datetime(
                current_time.year, current_time.month, current_time.day + 1, 0, 0, 0)
            seconds_to_tomorrow = tomorrow.timestamp() - current_time.timestamp() + 1
            print(f"Exceed the upload limitation (750GB). Sleep for {seconds_to_tomorrow} seconds until tomorrow")
            sleep(seconds_to_tomorrow)
            upload_file(folder_id, credentials_file, file)


if __name__ == '__main__':
    fire.Fire(main)
