from call_rest_api import driver
from flask import render_template, request

def index():
    return render_template("index.html")
def warlogInput():
    if request.method == 'GET':
        return render_template("warlogInput.html")
    if request.method == 'POST':
        clan_tag = request.form['clan_tag']
        jsonOut, response = driver("clans", clan_tag)
        if response != 404:
            return render_template(
            "warlogInput.html",
            clan_found = "true",
            clan_im = jsonOut["badgeUrls"]["medium"],
            description = jsonOut["description"],
            clan_level = jsonOut["clanLevel"],
            mem_count = jsonOut["members"]
        )
        else:
            return render_template("warlogInput.html", error = "Not Found")
def warlogSearchClan():
    return render_template("warlog.html")
def clan():
    return render_template("clan.html")