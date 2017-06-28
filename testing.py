import facebook

with open("/home/cabox/workspace/Facebook Stuff.txt") as file:
  secretInfo = file.readlines()

permAccessToken = secretInfo[0].strip('\n')
pageID = secretInfo[1].strip('\n')

GRAPH_VER = "2.9"

graph = facebook.GraphAPI(access_token=permAccessToken, version=GRAPH_VER) 

graph.put_object(
   parent_object = pageID,
   connection_name = "feed",
   message = "Testing Post Automation... Again")