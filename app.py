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
import os


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

def callApiCustom(method):
    headers = {'Authorization': 'Bearer '
                                'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjFiNmE3MmUxLTQ4YzMtNGVhYy1iZmE5LThmNzVjNDdjMzY5MCIsImlhdCI6MTY1MzA4MTA3Mywic3ViIjoiZGV2ZWxvcGVyL2M0YTVjMGQ3LTk5ZTQtZWE3OS02M2U1LWFkZTFmYjE4YTIzYyIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjk4LjYuMTE1LjE3NyJdLCJ0eXBlIjoiY2xpZW50In1dfQ.yuyorgS5JFvQX0YdypUhJYbkUWh0C2uJ2u2EwpgnucfaSBLACeTrK7v3KFYye-yzqTy-HK6cJaSQMDxcvr8Ruw'}
    endpoint = 'https://api.clashofclans.com/v1/clans/'
    clanTag = '%232QCJGUCJQ'
    addTag = '/'

    endpoint = endpoint + clanTag + addTag + method
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
   # total_stars = []
    for elem in jsonOut["clan"]["members"]:
        members.append(elem["name"])
        num_attacks.append(len(elem["attacks"]))
        avg_destruction = 0
        tot_stars = 0
        for nums in elem["attacks"]:
            avg_destruction += nums["destructionPercentage"]
            # tot_stars += nums["stars"]
        avg_destruction /= len(elem["attacks"])
        avg_dest.append(avg_destruction)
      #  total_stars.append(tot_stars)
    status = "At war"
    clan = jsonOut["clan"]["name"]
    opponent = jsonOut["opponent"]["name"]
    enem_stars = jsonOut["opponent"]["stars"]
    total_stars = jsonOut["clan"]["stars"]
    return clan, opponent, members, num_attacks, avg_dest, total_stars, enem_stars, status

def getImage():
    jsonOut = callApi()

    # names = []
    th_level = []
    avg_dest = []
    for elem in jsonOut["clan"]["members"]:
        # names.append(elem["name"])
        th_level.append(elem["townhallLevel"])
        avg_destruction = 0
        for attacks in elem["attacks"]:
            avg_destruction += attacks["destructionPercentage"]
        avg_destruction /= len(elem["attacks"])
        avg_dest.append(avg_destruction)

    unique_th = []
    for x in th_level:
        if x not in unique_th:
            unique_th.append(x)

    unique_th_dest = []
    counts = []
    for k in unique_th:
        counts.append(th_level.count(k))
        sum = 0
        for index, th in enumerate(th_level):
            if th == k:
                sum += avg_dest[index]
        unique_th_dest.append(sum/th_level.count(k))

    unique_th, unique_th_dest = zip(*sorted(zip(unique_th, unique_th_dest)))

    width = 0.35
    fig = Figure()
    ax = fig.subplots()
    ax.bar(unique_th, unique_th_dest, width, color="yellow", linewidth=0.75)
    ax.set(xlabel='Townhall Level', ylabel='Average Destruction Percentage',
    title='Average Attack Destruction by Townhall Level')
    ax.set_facecolor("white")
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

def getWarlogPlotData():
    jsonOut = callApiCustom("warlog")

    us_dest = []
    them_dest = []
    won = []
    for index, elem in enumerate(jsonOut["items"]):
        u_dest = int(elem["clan"]["destructionPercentage"])
        us_dest.append(u_dest)
        t_dest = int(elem["opponent"]["destructionPercentage"])
        them_dest.append(t_dest)
        if elem["result"] == "lose":
            won.append("War " + str(index+1) + ": Lost")
        elif elem["result"] == "win":
            won.append("War " + str(index+1) + ": Won")
        else: 
            won.append("War " + str(index+1) + ": Hold this")
    x = np.arange(len(won))

    width = 0.35
    fig = Figure()
    ax = fig.subplots()
    rects1 = ax.bar(x - width/2, us_dest, width, color = "blue", linewidth=0.75, label='Clan')
    rects2 = ax.bar(x + width/2, them_dest, width, color = "red", linewidth=0.75, label='Opponent')
    ax.set_ylabel('Destruction Percentage')
    ax.set_title('Clan vs Opponent Destruction Percentage Per War')
    ax.set_xticks(x, won)
    ax.legend()
    ax.set_facecolor("white")
    ax.bar_label(rects1, padding=3)
    ax.bar_label(rects2, padding=3)
    ax.set_xticklabels(won, rotation = 30)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/warstatus")
def warstatus():
    status = checkWarStatus()
    if status == "preparation":
        data1 = getWarlogPlotData()
        clan_name, opponent_name, status, time_left = prepStage()
        return render_template(
                "dataVis.html",
                clan_name = clan_name,
                opponent_name = opponent_name,
                status = status,
                time = time_left,
                graph = f"data:image/png;base64,{data}"
        )
    elif status == "inWar":
        data = getImage()
        data1 = getWarlogPlotData()
        clan_name, opponent_name, members, num_attacks, avg_dest, total_stars, their_stars, status = warStage()
        return render_template(
                "dataVisWar.html",
                clan_name = clan_name,
                opponent_name = opponent_name,
                status = status,
                stars_won = total_stars,
                their_stars = their_stars,
                graph2 = f"data:image/png;base64,{data}",
                graph1 = f"data:image/png;base64,{data1}"
        )
    else:
        return render_template("layout.html")
     
@app.route("/clan")
def clan():
    clan_name, opponent_name, members, num_attacks, avg_dest, total_stars, their_stars, status = warStage()
    return render_template("dataVisClan.html",
                            clan_name = clan_name,
                            opponent_name = opponent_name,
                            status = status,
                            stars_won = total_stars,
                            their_stars = their_stars)
