import pip._vendor.requests
import json

def cleanTag(input):
    output = input[1:len(input)]
    output = "%23" + output
    return output

def driver(method, tag):
    headers = {'Authorization': 'Bearer '}
    broad_endpoint = 'https://api.clashofclans.com/v1/'
    tag = cleanTag(tag)
    if method == "members" or method == "currentwar" or method == "warlog":
        signifier = 'clans/'
        this_endpoint = broad_endpoint + signifier
        this_endpoint = this_endpoint + tag + '/' + method
    elif method == "players":
        signifier = 'players/'
        this_endpoint = broad_endpoint + signifier
        this_endpoint = this_endpoint + tag
    elif method == "clans":
        signifier = 'clans/'
        this_endpoint = broad_endpoint + signifier + tag

    response = pip._vendor.requests.get(this_endpoint, headers=headers).text
    jsonOut = json.loads(response)
    
    responseCode = 101
    if 'reason' in jsonOut:
        if jsonOut['reason'] == 'notFound':
            responseCode = 404
    
    return jsonOut, responseCode