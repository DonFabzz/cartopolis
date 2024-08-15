import requests
import gzip
import shutil
import os
from .models import Islands, init_db, Towns, Alliances, Players
from config import URL_ISLANDS, URL_TOWNS, URL_ALLIANCES, URL_PLAYERS
import csv
import logging
from . import db
from sqlalchemy import text
import urllib.parse



def downloadsItems(items, token):

    if token != 'e4f8cba86214ae062d14ddc9afb7c03f' :
        return False

    match items:
        case 'islands':
            response = requests.get(URL_ISLANDS, stream=True)
        case 'towns':
            response = requests.get(URL_TOWNS, stream=True)
        case 'players':
            response = requests.get(URL_PLAYERS, stream=True)
        case 'alliances':
            response = requests.get(URL_ALLIANCES, stream=True)
        case _:
            return False

    if os.makedirs('tmp', exist_ok=True):
        return False
    
    with open(f"tmp/{items}.txt.gz", 'wb') as file:
        file.write(response.content)

    with gzip.open(f'tmp/{items}.txt.gz', 'rb') as fIn:
        with open(f'tmp/{items}.txt', 'wb') as fOut:
            shutil.copyfileobj(fIn, fOut)

    os.remove(f"tmp/{items}.txt.gz")
    db.session.execute(text(f'DELETE FROM {items}'))

    with open (f'tmp/{items}.txt') as txtFile:
        for line in txtFile:
            datas = line.split(',')
            match items:
                case 'islands':
                    db.session.add(Islands(datas[0], datas[1], datas[2], datas[3], datas[4]))
                case 'towns':
                    db.session.add(Towns(datas[0], datas[1], urllib.parse.unquote(str(datas[2])).replace("'", " ").replace('+', ' '), datas[3], datas[4], datas[5], datas[6]))
                case 'players':
                    db.session.add(Players(datas[0], urllib.parse.unquote(str(datas[1])).replace("'", " ").replace('+', ' '), datas[2], datas[3], datas[4], datas[5]))
                case 'alliances':
                    db.session.add(Alliances(datas[0], urllib.parse.unquote(str(datas[1])).replace("'", " ").replace('+', ' '), datas[2], datas[3], datas[4], datas[5]))

    db.session.commit()

    os.remove(f"tmp/{items}.txt")

    return True

def deleteItems(items):
    init_db