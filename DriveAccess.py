from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

import re

CREDENTIALS_PATH = "/home/cabox/workspace/Drive Credentials.txt"

class DriveAccessor(object):

  def __init__(self, mainID, backupID):
    self.ANIMEMES_FOLDER_ID = mainID
    self.BACKUP_FOLDER_ID = backupID
    
    self.gauth = GoogleAuth()
    self.gauth.LoadCredentialsFile(CREDENTIALS_PATH);
    self.authorize()
    self.drive = GoogleDrive(self.gauth)

  def authorize(self):
      if self.gauth.credentials is None:
        print("No Credentials...")
        self.gauth.GetFlow()
        self.gauth.flow.params.update({'access_type': 'offline'})
        self.gauth.flow.params.update({'approval_prompt': 'force'})
        self.gauth.LocalWebserverAuth()
      elif self.gauth.access_token_expired:
        print("Credentials Expired")
        self.gauth.Refresh()
      else:
        print("Credentials are good, authorizing...")
        self.gauth.Authorize()
      
      self.gauth.SaveCredentialsFile(CREDENTIALS_PATH)
      
  def downloadMeme(self):
    fileList = self.drive.ListFile({'q': "'" + self.ANIMEMES_FOLDER_ID + "' in parents and trashed=false"}).GetList()
    imgPattern = re.compile("image.*")

    for file in fileList:
      if imgPattern.match(file["mimeType"]):
        fileType = file["mimeType"].split('/')[-1]
        print("Got image", file["title"])
        self.imgFile = self.drive.CreateFile({'id' : file['id']})
        self.imgFile.GetContentFile("ToUpload." + fileType)
        break

#file1 = drive.CreateFile({'title': 'Hello.txt'})
#file1.Upload()