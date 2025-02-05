# Google drive api

## Installation

```bash
pip install -r requirements.txt
```

## Prepare credentials

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Go to the project
4. Go to the `APIs & Services` -> enable `Google Drive API`
5. Go to the `Credentials` -> create credentials -> `Build on oAuth2.0` -> `Desktop app`
6. Download the credentials json and put it in the root of the project as `credentials.json`

## Usage

### Upload file

```bash
ipython -- src/upload.py
	--file_path <file_path>					# file path
	--folder_id <folder_id> 				# folder id
	--credentials_file <credentials_file>	# credentials file, default="credentials.json"
```

### Upload folder

```bash
# if you want to upload inside a existing folder, you need to give mother folder id
ipython -- src/upload_folder.py
	--folder <folder_path>					# folder path
	--mother_folder_id <mother_folder_id>	# mother folder id
	--credentials_file <credentials_file>	# credentials file, default="credentials.json"
```

### Download file

```bash
ipython -- src/download.py
	--file_id <file_id> 			# file id
	--dst_path <file_path>			# destination path
	--credentials_file <credentials_file>	# credentials file, default="credentials.json"
```

### Download folder

```bash
ipython -- src/download_folder.py
	--folder_id <folder_id>					# folder id
	--dst_folder <folder_path> 				# destination folder
	--credentials_file <credentials_file>	# credentials file, default="credentials.json"
	--scan_size <scan_size> 				# number of files to scan
```
