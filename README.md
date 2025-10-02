# UpDownGDrive

This repository provides a tool for uploading and downloading files to and from Google Drive. It uses personal credentials to access both individual and shared drives, allowing seamless transfer of folders and files.

## Installation

```bash
pip install -r requirements.txt
```

## **Prepare credentials**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Go to the project
4. Go to the `APIs & Services` -> enable `Google Drive API`
5. Go to the `Credentials` -> create credentials -> `Build on oAuth2.0` -> `Desktop app`
6. Download the credentials json and put it in the root of the project as `credentials.json`

## Usage

### Upload a file

```bash
file_path="path/to/file"
folder_id="folder_id"
credentials_file="path/to/credentials.json"
ipython -- src/upload.py \
    --file_path $file_path \
    --folder_id $folder_id \
    --credentials_file $credentials_file
```

### Upload a folder

```bash
folder="path/to/folder"
mother_folder_id="mother_folder_id"
# if you want to upload inside a existing folder, you need to give mother folder id
credentials_file="path/to/credentials.json"
ipython -- src/upload_folder.py \
    --folder $folder \
    --mother_folder_id $mother_folder_id \
    --credentials_file $credentials_file
```

### Download a file

```bash
file_id="file_id"
dst_path="path/to/save"
credentials_file="path/to/credentials.json"
ipython -- src/download.py \
    --file_id $file_id \
    --dst_path $dst_path \
    --credentials_file $credentials_file
```

### Download a folder

```bash
folder_id="folder_id"
dst_folder="path/to/save"
credentials_file="path/to/credentials.json"
scan_size=1000
ipython -- src/download_folder.py \
    --folder_id $folder_id \
    --dst_folder $dst_folder \
    --credentials_file $credentials_file \
    --scan_size $scan_size
```
