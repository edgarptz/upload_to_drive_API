from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import argparse
import os

# Đường dẫn đến file `credential.json` đã tải xuống từ Google Cloud Console
SERVICE_ACCOUNT_FILE = 'credential.json'

SCOPES = ['https://www.googleapis.com/auth/drive.file']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('drive', 'v3', credentials=credentials)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=str, default = "./data", help="Path to the  data directory ")
    parser.add_argument("--folder-id", type=str, default = None, help="folder ID in drive")

    return parser.parse_args()

def upload_file_to_drive(data_dir, drive_folder_id=None):
    """

    :param data_dir: Data directory contains files want to upload.
    :param drive_folder_id: ID of folder in Drive want to upload to.
    :return: ID of file uploaded.
    """
    uploaded_file_ids = []

    for file_path in os.listdir(data_dir):
        file_metadata = {'name': file_path.split('/')[-1]}
        if drive_folder_id:
            file_metadata['parents'] = [drive_folder_id]

        media = MediaFileUpload(os.path.join(data_dir,file_path), resumable=True)

        request = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        )

        file = request.execute()

        uploaded_file_ids.append(file['id'])
        print(f"File {file_path} uploaded to Drive with ID: {file['id']}\n")

    return uploaded_file_ids

def main():
    args = parse_args()

    data_dir = args.data_dir
    folder_id = args.folder_id

    upload_file_to_drive(data_dir=data_dir,drive_folder_id=folder_id)

if __name__=='__main__':
    main()
