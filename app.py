from flask import Flask
import datetime
from flask import render_template, request
from flask_table import Table, Col
import pip._vendor.requests
import json
from dateutil import parser
import io
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


# https://code.visualstudio.com/docs/python/tutorial-flask

class PlayerTable(Table):
    name = Col('Name')
    num_att = Col('Number of Attacks')

def callApi():
    headers = {'Authorization': 'Bearer '
                                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFiNmE3MmUxLTQ4YzMtNGVhYy1iZmE5LThmNzVjNDdjMzY5MCIsImlhdCI6MTY1MzA4MTA3Mywic3ViIjoiZGV2ZWxvcGVyL2M0YTVjMGQ3LTk5ZTQtZWE3OS02M2U1LWFkZTFmYjE4YTIzYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjYuMTE1LjE3NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yuyorgS5JFvQX0YdypUhJYbkUWh0C2uJ2u2EwpgnucfaSBLACeTrK7v3KFYye-yzqTy-HK6cJaSQMDxcvr8Ruw'}
    endpoint = 'https://api.clashofclans.com/v1/clans/'
    clanTag = '%232QCJGUCJQ'
    addTag = '/'
    apiMethod = 'currentwar'

    endpoint = endpoint + clanTag + addTag + apiMethod
    response = pip._vendor.requests.get(endpoint, headers=headers).text
    jsonOut = json.loads(response)
    
    return jsonOut

def checkWarStatus():
    jsonOut = callApi()
    return jsonOut["state"]

def prepStage():
    jsonOut = callApi()

    intput_string = jsonOut["endTime"]
    year = int(intput_string[0:4])
    month = int(intput_string[4:6])
    day = int(intput_string[6:8])
    hour = int(intput_string[10:13])
    min_l = int(intput_string[10:13])
    date_l = datetime.datetime(year, month, day, hour, min_l)
    date_curr = datetime.datetime.now()
    time_left = str(date_l - date_curr)
    status = "Preparing for war."

    return jsonOut["clan"]["name"], jsonOut["opponent"]["name"], status, time_left

def warStage():
    jsonOut = callApi()

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
    enem_stars = jsonOut["opponent"]["stars"]
    return clan, opponent, members, num_attacks, avg_dest, total_stars, enem_stars, status

def getImage():
    headers = {'Authorization': 'Bearer '
                                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFiNmE3MmUxLTQ4YzMtNGVhYy1iZmE5LThmNzVjNDdjMzY5MCIsImlhdCI6MTY1MzA4MTA3Mywic3ViIjoiZGV2ZWxvcGVyL2M0YTVjMGQ3LTk5ZTQtZWE3OS02M2U1LWFkZTFmYjE4YTIzYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjYuMTE1LjE3NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yuyorgS5JFvQX0YdypUhJYbkUWh0C2uJ2u2EwpgnucfaSBLACeTrK7v3KFYye-yzqTy-HK6cJaSQMDxcvr8Ruw'}
    endpoint = 'https://api.clashofclans.com/v1/clans/'
    clanTag = '%232QCJGUCJQ'
    addTag = '/'
    apiMethod = 'warlog'

    endpoint = endpoint + clanTag + addTag + apiMethod
    response = pip._vendor.requests.get(endpoint, headers=headers).text
    jsonOut = json.loads(response)

    ctr = 0
    wars = []
    for elem in jsonOut["items"]:
        wars.append(elem["clan"]["attacks"])
        ctr += 1

    wars_num = len(wars)
    fig = Figure()
    ax = fig.subplots()
    ax.plot(range(wars_num),wars)
    ax.set(xlabel='Wars', ylabel='Num Attacks',
    title='Number of Attacks per War')
    ax.grid()
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    data = base64.b64encode(buffer.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
    

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/warstatus")
def warstatus():
    status = checkWarStatus()
    if status == "preparation":
        clan_name, opponent_name, status, time_left = prepStage()
        return render_template(
                "dataVis.html",
                clan_name = clan_name,
                opponent_name = opponent_name,
                status = status,
                time = time_left
        )
    elif status == "inWar":
        clan_name, opponent_name, members, num_attacks, avg_dest, total_stars, their_stars, status = warStage()
        total_s = sum(total_stars)
        return render_template(
                "dataVisWar.html",
                clan_name = clan_name,
                opponent_name = opponent_name,
                status = status,
                stars_won = total_s,
                their_stars = their_stars
        )
    else:
        return render_template("layout.html")
    

@app.route("/demo")
def demo():
    this_image = getImage()

    return render_template(
        "showGraph.html",
        image = this_image
    )
