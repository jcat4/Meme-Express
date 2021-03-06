from PageAccess import PageAccessor
from DriveAccess import DriveAccessor

import json
import os

NO_MEMES_MSG = "No memes to post :("
DONE_MSG     = "All done!"

fileDir = "Meme Express Info.json"
#fileDir = "/home/cabox/workspace/Meme Express Info.json" # development

with open(fileDir) as secretFile:
  data = json.load(secretFile)

# initiate
pageAccessor = PageAccessor( \
  data["facebook"]["token"], \
  data["facebook"]["page_id"])
driveAccessor = DriveAccessor(\
  data["drive"]["anime_folder_id"], \
  data["drive"]["backup_folder_id"], \
  data["drive"]["queue_folder_id"])

# Grab and download meme, if any
imgName = driveAccessor.getMeme()

# Post meme if available
if imgName is None:
  print(NO_MEMES_MSG)
else:
  pageAccessor.postImage(imgName)
  driveAccessor.backupMeme(imgName)
  os.remove(imgName)
  
print(DONE_MSG)