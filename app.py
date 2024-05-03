from flask import Flask, request, jsonify
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = "service_account.json"

credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

@app.route('/', methods=['POST'])
def upload_files():
    uploaded_files = request.files.getlist('file')  # Get a list of all the uploaded files
    if not uploaded_files:
        return jsonify({'error': 'No files provided'}), 400

    service = build('drive', 'v3', credentials=credentials)
    upload_responses = []

    for file in uploaded_files:
        if file and file.filename:
            file_metadata = {'name': file.filename}
            media = MediaFileUpload(file.filename, mimetype=file.content_type)
            uploaded_file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            upload_responses.append({'fileId': uploaded_file.get('id')})

    return jsonify(upload_responses)

if __name__ == '__main__':
    app.run(port=5000, debug=True)