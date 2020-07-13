import requests, time, math, json, argparse

_G_TOKEN = "42323d64886122307be10013ad2dcc44"

def getUserMeta(username):
  metaUrl = "https://www.instagram.com/" + str(username) + "/?__a=1"
  getMeta = requests.get(metaUrl)
  parsedMeta = getMeta.json()

  returnMeta = {
    "id": parsedMeta['graphql']['user']['id'],
    "is_verified": parsedMeta['graphql']['user']['is_verified'],
    "full_name": parsedMeta['graphql']['user']['full_name'],
    "biography": parsedMeta['graphql']['user']['biography'],
    "profile_pic_url": parsedMeta['graphql']['user']['profile_pic_url'],
    "profile_pic_url_hd": parsedMeta['graphql']['user']['profile_pic_url_hd'],
    "external_url": parsedMeta['graphql']['user']['external_url'],
    "edge_owner_to_timeline_media": parsedMeta['graphql']['user']['edge_owner_to_timeline_media']['count']
  }
  return returnMeta

def fetchUserContent(userMeta):
  fetchRequest1st = requests.get("https://www.instagram.com/graphql/query/?query_hash="+_G_TOKEN+"&variables=%7B%22id%22:%22"+userMeta["id"]+"%22,%22first%22:%2250%22%7D")
  parsedReq = fetchRequest1st.json()

  nextToken = ""
  fetchedData = []

  if parsedReq["data"]["user"]["edge_owner_to_timeline_media"]["count"] > 50:
    for x in range(math.ceil(parsedReq["data"]["user"]["edge_owner_to_timeline_media"]["count"]/50)):
      fetchDatawToken = requests.get("https://www.instagram.com/graphql/query/?query_hash="+_G_TOKEN+"&variables=%7B%22id%22:%22"+userMeta["id"]+"%22,%22first%22:%2250%22,%22after%22:%22"+nextToken+"%22%7D")
      dataRaw = fetchDatawToken.json()
      nextToken = dataRaw["data"]["user"]["edge_owner_to_timeline_media"]["page_info"]["end_cursor"]
      fetchedData += dataRaw["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

    
    return fetchedData
  else:
    return parsedReq["data"]["user"]["edge_owner_to_timeline_media"]["edges"]

  print(fetchRequest1st)

def writeUserContent(userMeta, data):
  with open(str(userMeta["id"])+"_exported_"+str(time.time())+".json", 'w', newline='') as fileJson:
    json.dump(data, fileJson)

parser = argparse.ArgumentParser()

parser.add_argument("user", help="instagram username for dump data")

args = parser.parse_args()

userMeta = getUserMeta(args.user)
fetchData = fetchUserContent(userMeta)
writeUserContent(userMeta, fetchData)
