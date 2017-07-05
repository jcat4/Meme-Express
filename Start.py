from PageAccess import PageAccessor
from DriveAccess import DriveAccessor

import json

fileDir = "/home/cabox/workspace/Meme Express Info.json"
with open(fileDir) as secretFile:
  data = json.load(secretFile)

# initiate
pageAccessor = PageAccessor(\
  data["facebook"]["token"], \
  data["facebook"]["page_id"])
driveAccessor = DriveAccessor(\
  data["drive"]["test_folder_id"], \
  data["drive"]["test_backup_folder_id"])

# Grab and download meme, if any
driveAccessor.downloadMeme()

# Post meme to facebook page
pageAccessor.postImage()