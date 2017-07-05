from PageAccess import PageAccessor
from DriveAccess import DriveAccessor

import json

fileDir = "/home/cabox/workspace/Meme Express Info.json"
with open(fileDir) as secretFile:
  data = json.load(secretFile)
  fbData = data["facebook"]
  driveData = data["drive"]

# initiate
pageAccessor = PageAccessor(\
  fbData["token"], \
  fbData["page_id"])
driveAccessor = DriveAccessor(\
  driveData["test_folder_id"], \
  driveData["test_backup_folder_id"])

# Grab and download meme, if any
driveAccessor.downloadMeme()

# Post meme to facebook page
pageAccessor.postImage()