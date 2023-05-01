import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://drive.google.com/drive/folders']

# 1-ZWvNv9_MgWg_OXC4N1xLFmT8PCws3v6

credentials = service_account.Credentials.from_service_account_file(
  'C:/credentials.json'
)
service = None

def init():
    global service
    service = build('drive', 'v3', credentials=credentials)

def createRootFolder():
    # folder details we want to make
    folder_metadata = {
        "name": "ChromeEXT-Reviews",
        "mimeType": "application/vnd.google-apps.folder"
    }

    # create the folder
    file = service.files().create(body=folder_metadata, fields="id").execute()
    # get the folder id
    folder_id = file.get("id")
    # folder_id = "1tbmX2fjiluQ_YOzPTKCUAOZA0y2uch_N"
    print("Folder ID:", folder_id)
    return folder_id

def upload_reviews(folder_id, src_path, file_name):

# Call the Drive v3 API
# results = service.files().list( fields="nextPageToken, files(id, name)").execute()

    # upload a file text file
    # first, define file metadata, such as the name and the parent folder ID
    file_metadata = {
        "name": file_name,
        "parents": [folder_id]
    }
    # upload
    media = MediaFileUpload(src_path, resumable=True)
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print("File created, id:", file.get("id"))


init()
# createRootFolder() 1Mq8cbu1CQ3wx40NPYBrzneMS8q4ZXGfg