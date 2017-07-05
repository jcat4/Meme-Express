import facebook

GRAPH_VER = "2.9"

class PageAccessor(object):

  def __init__(self, token, pageID):
    self.graph = facebook.GraphAPI(access_token=token, version=GRAPH_VER)
    self.pageID = pageID
    print("Got Facebook Page access")

  def postStatus(self, passedMessage):
    self.graph.put_object(
       parent_object = self.pageID,
       connection_name = "feed",
       message = passedMessage)
    
  def postImage(self):
    print("*posts image* (Not implemented yet!)")