from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from random import shuffle

import re

CREDENTIALS_PATH = "Drive Credentials.txt"
#CREDENTIALS_PATH = "/home/cabox/workspace/Drive Credentials.txt" # development

# Credentials Constants
NO_CREDENTIALS_MSG   = "No Credentials..."
EXPIRED_CREDS_MSG    = "Credentials Expired"
REFRESHED_CREDS_MSG  = "Credentials Refreshed"
VALID_CREDS_MSG      = "Credentials are good, authorizing..."
ACCESS_TYPE_DICT     = { 'access_type': 'offline' }
APPROVAL_PROMPT_DICT = { 'approval_prompt': 'force' }

# getMeme Constants
INIT_DOWNLOAD_MSG = "Attempting to download file..."
EMPTY_QUEUE_MSG   = "No files in queue, grabbing random image from main folder"
GOT_IMAGE_MSG     = "Got image"

# backupMeme Constants
BACKUP_IMAGE_MSG = "Backing up file..."

class DriveAccessor(object):

  def __init__(self, mainID, backupID, queueID):
    self.ANIMEMES_FOLDER_ID = mainID
    self.BACKUP_FOLDER_ID   = backupID
    self.QUEUE_FOLDER_ID    = queueID
    
    self.gauth = GoogleAuth()
    self.gauth.LoadCredentialsFile(CREDENTIALS_PATH);
    self.authorize()
    self.drive = GoogleDrive(self.gauth)

  def authorize(self):
      if self.gauth.credentials is None:
        print(NO_CREDENTIALS_MSG)
        self.gauth.GetFlow()
        self.gauth.flow.params.update(ACCESS_TYPE_DICT)
        self.gauth.flow.params.update(APPROVAL_PROMPT_DICT)
        self.gauth.LocalWebserverAuth()
      elif self.gauth.access_token_expired:
        print(EXPIRED_CREDS_MSG)
        self.gauth.Refresh()
        print(REFRESHED_CREDS_MSG)
      else:
        print(VALID_CREDS_MSG)
        self.gauth.Authorize()
      
      self.gauth.SaveCredentialsFile(CREDENTIALS_PATH)
      
  def getMeme(self):
    print(INIT_DOWNLOAD_MSG)
    fileList = self.drive.ListFile({ 
        'q': self.getFileQuery(self.QUEUE_FOLDER_ID) 
      }).GetList()
    
    # Queued Folder is empty, use regular meme folder and shuffle
    if not fileList:
      print(EMPTY_QUEUE_MSG)
      fileList = self.drive.ListFile({ 
        'q': self.getFileQuery(self.ANIMEMES_FOLDER_ID) 
      }).GetList()
      shuffle(fileList)
      
    imgPattern = re.compile("image.*")

    for file in fileList:
      if imgPattern.match(file["mimeType"]):
        imgName = file["title"]
        print(GOT_IMAGE_MSG, imgName)
        self.imgFile = self.drive.CreateFile({ 'id' : file['id'] })
        self.imgFile.GetContentFile(imgName)
        return imgName
    return None
        
  def backupMeme(self, imgName):
    print(BACKUP_IMAGE_MSG)
    backupFile = self.drive.CreateFile({
      "parents": [{ "kind": "drive#fileLink", "id": self.BACKUP_FOLDER_ID }]
    }) 
    backupFile.SetContentFile(imgName)
    backupFile.Upload()
    self.imgFile.Delete()
    
  def getFileQuery(self, folderID):
    return ("'" + folderID + "' in parents and trashed=false")