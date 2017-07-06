from PageAccess import PageAccessor
from DriveAccess import DriveAccessor

import json
import os

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
imgName = driveAccessor.getMeme()

# Post meme if available
if imgName is None:
  print("No memes to post :(")
else:
  pageAccessor.postImage(imgName)
  driveAccessor.backupMeme(imgName)
  os.remove(imgName)
  
print("All done!")