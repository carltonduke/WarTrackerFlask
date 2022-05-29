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
    headers = {'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFiNmE3MmUxLTQ4YzMtNGVhYy1iZmE5LThmNzVjNDdjMzY5MCIsImlhdCI6MTY1MzA4MTA3Mywic3ViIjoiZGV2ZWxvcGVyL2M0YTVjMGQ3LTk5ZTQtZWE3OS02M2U1LWFkZTFmYjE4YTIzYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjYuMTE1LjE3NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yuyorgS5JFvQX0YdypUhJYbkUWh0C2uJ2u2EwpgnucfaSBLACeTrK7v3KFYye-yzqTy-HK6cJaSQMDxcvr8Ruw'}
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