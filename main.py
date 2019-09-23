import openpyxl

import os


import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.http import MediaFileUpload




# data = pd.read_excel (r'Video_List.xlsx')
# df = pd.DataFrame(data, columns= ['Title','Author'])
# print(df)

video_wb=openpyxl.load_workbook("Video_List.xlsx")
sheet=video_wb.active






CLIENT_SECRETS_FILE="client_secrets.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = 'v3'

def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

if __name__ == '__main__':
      # When running locally, disable OAuthlib's HTTPs verification. When
      # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()

    request = service.videos().insert(
        part="snippet,status",
        autoLevels=True,
        notifySubscribers=True,
        stabilize=True,
        body={
          "snippet": {
            # "categoryId": "22",
            "description": "Description of uploaded video.",
            "title": "Area 51 raid."
          },
          "status": {
            "privacyStatus": "public"
          }
        },
        # TODO: For this request to work, you must replace "YOUR_FILE"
        #       with a pointer to the actual file you are uploading.
        media_body=MediaFileUpload("IMG_1020.mp4", mimetype='video/mp4')
    )

    response = request.execute()
    print(response)



