import facebook

GRAPH_VER = "2.9"

ACCESS_SUCCESS_MSG = "Got Facebook Page access"
UPLOAD_SUCCESS_MSG = "photo uploaded"

class PageAccessor(object):

  def __init__(self, token, pageID):
    self.graph = facebook.GraphAPI(access_token=token, version=GRAPH_VER)
    self.pageID = pageID
    print(ACCESS_SUCCESS_MSG)

  def postStatus(self, passedMessage):
    self.graph.put_object(
       parent_object = self.pageID,
       connection_name = "feed",
       message = passedMessage)
    
  def postImage(self, imgName):
    self.graph.put_photo(image=open(imgName, 'rb'))
    print(UPLOAD_SUCCESS_MSG)