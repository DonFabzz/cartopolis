from flask import Flask, render_template, request
from .cron import downloadsItems, deleteItems
from . import app
from .utils import getIslandCentral, getTownsCentral, serialize_island, serialize_town, getTopAlliances, getOuterIsland, getOuterTowns
import json

app.config.from_object('config')

@app.route('/')
def displayMap():
    towns = getTownsCentral()
    serialized_towns= [serialize_town(town, island, player, alliance) for town, island, player, alliance in towns]
    towns_json = json.dumps(serialized_towns)

    alliances = getTopAlliances()

    return render_template('map.html', towns=towns_json, alliances=alliances)

@app.route('/downloadsData')
def downloadsData():
    data_type = request.args.get('data_type')
    token = request.args.get('token')

    value = downloadsItems(data_type, token)
    
    if value == True:
        return 'true'
    else:
        return 'false'
    
@app.route('/loadMainIslands')
def loadIsland():
    islands = getIslandCentral()
    serialized_islands = [serialize_island(island) for island in islands]
    islands_json = json.dumps(serialized_islands)
    return islands_json

@app.route('/loadRemainsTowns')
def loadTown():
    towns = getOuterTowns()
    serialized_towns= [serialize_town(town, island, player, alliance) for town, island, player, alliance in towns]
    towns_json = json.dumps(serialized_towns)
    return towns_json
    
@app.route('/deleteDatas')
def deleteDatas():
    data_type = request.args.get('data_type')
    if data_type == 'islands' or data_type == 'towns':
        value = deleteItems(data_type)

    return 'ok'

if __name__ == "__main__":
    app.run()