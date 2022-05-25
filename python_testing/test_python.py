import pip._vendor.requests
import json
import matplotlib.pyplot as plt
import numpy as np

headers = {'Authorization': 'Bearer '
                                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFiNmE3MmUxLTQ4YzMtNGVhYy1iZmE5LThmNzVjNDdjMzY5MCIsImlhdCI6MTY1MzA4MTA3Mywic3ViIjoiZGV2ZWxvcGVyL2M0YTVjMGQ3LTk5ZTQtZWE3OS02M2U1LWFkZTFmYjE4YTIzYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjYuMTE1LjE3NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yuyorgS5JFvQX0YdypUhJYbkUWh0C2uJ2u2EwpgnucfaSBLACeTrK7v3KFYye-yzqTy-HK6cJaSQMDxcvr8Ruw'}
endpoint = 'https://api.clashofclans.com/v1/clans/'
clanTag = '%232QCJGUCJQ'
addTag = '/'
apiMethod = 'warlog'

endpoint = endpoint + clanTag + addTag + apiMethod
response = pip._vendor.requests.get(endpoint, headers=headers).text
jsonOut = json.loads(response)

wars = []
for elem in jsonOut["items"]:
    wars.append(elem["clan"]["attacks"])

print(wars)

wars_num = len(wars)
fig, ax = plt.subplots()
ax.plot(range(wars_num),wars)
ax.set(xlabel='Wars', ylabel='Num Attacks',
        title='Number of Attacks per War')
ax.grid()
fig.savefig("test.png")
plt.show()

endpoint = 'https://api.clashofclans.com/v1/clans/'
clanTag = '%232QCJGUCJQ'
addTag = '/'
apiMethod = 'currentwar'

endpoint = endpoint + clanTag + addTag + apiMethod
response = pip._vendor.requests.get(endpoint, headers=headers).text
jsonOut = json.loads(response)

members = []
num_attacks = []
avg_dest = []
total_stars = []
for elem in jsonOut["clan"]["members"]:
    members.append(elem["name"])
    num_attacks.append(len(elem["attacks"]))
    avg_destruction = 0
    tot_stars = 0
    for nums in elem["attacks"]:
        avg_destruction += nums["destructionPercentage"]
        tot_stars += nums["stars"]
    avg_destruction /= len(elem["attacks"])
    avg_dest.append(avg_destruction)
    total_stars.append(tot_stars)
status = "At war."
clan = jsonOut["clan"]["name"]
opponent = jsonOut["opponent"]["name"]