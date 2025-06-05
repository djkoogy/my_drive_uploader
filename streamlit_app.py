import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os, tempfile

def authenticate_drive():
    gauth = GoogleAuth()
    gauth.LoadServiceConfigFile("settings.yaml")
    gauth.Authorize()
    return GoogleDrive(gauth)

def upload_to_drive(uploaded_file, drive_folder_id):
    drive = authenticate_drive()
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    file_drive = drive.CreateFile({
        'title': uploaded_file.name,
        'parents': [{'id': drive_folder_id}]
    })
    file_drive.SetContentFile(tmp_file_path)
    file_drive.Upload()
    os.remove(tmp_file_path)
    return file_drive['id']

st.title("📤 Google Drive 파일 업로더")
uploaded_file = st.file_uploader("파일을 업로드하세요")

if uploaded_file:
    folder_id = "여기에_당신의_Google_Drive_폴더_ID"
    file_id = upload_to_drive(uploaded_file, folder_id)
    st.success(f"업로드 완료! Google Drive 파일 ID: {file_id}")
