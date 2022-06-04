import pip._vendor.requests
import json

def cleanTag(input):
    ouput = input
    if input[0] == "#":
        output = input[1:len(input)]
        output = "%23" + input
    else:
        output = "%23" + input
    return output

def driver(method, tag):
    headers = {'Authorization': ''}
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
    
    return jsonOut, pip._vendor.requests.get(this_endpoint, headers=headers).status_code
