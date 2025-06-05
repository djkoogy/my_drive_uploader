import streamlit as st
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import tempfile
import json
import os

# ⬇️ 1. 서비스 계정 정보 읽기
service_account_info = st.secrets["google_service_account"]

# ⬇️ 2. 임시 JSON 파일로 저장
with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix=".json") as f:
    json.dump(service_account_info, f)
    service_account_path = f.name

# ⬇️ 3. PyDrive 인증
gauth = GoogleAuth()
gauth.LoadServiceConfigFile("settings.yaml")
gauth.credentials = gauth.service_account_credentials(service_account_path)
drive = GoogleDrive(gauth)

# ⬇️ 4. Google Drive 업로드 함수
def upload_to_drive(uploaded_file, folder_id):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    file_drive = drive.CreateFile({
        'title': uploaded_file.name,
        'parents': [{'id': folder_id}]
    })
    file_drive.SetContentFile(tmp_file_path)
    file_drive.Upload()
    os.remove(tmp_file_path)
    return file_drive['id']

# ⬇️ 5. Streamlit UI
st.title("📤 Google Drive 파일 업로더")

uploaded_file = st.file_uploader("파일을 선택하세요")

if uploaded_file:
    # Google Drive 폴더 ID 입력 (Google Drive 폴더 공유 설정 필요)
    folder_id = "여기에_당신의_Google_Drive_폴더_ID"  # 예: "1abCDeFG_hiJKlmnOPQrStUvWxYz"
    
    try:
        file_id = upload_to_drive(uploaded_file, folder_id)
        st.success(f"✅ 업로드 완료! 파일 ID: {file_id}")
        st.markdown(f"[📎 Google Drive에서 열기](https://drive.google.com/file/d/{file_id})")
    except Exception as e:
        st.error(f"❌ 업로드 실패: {e}")
