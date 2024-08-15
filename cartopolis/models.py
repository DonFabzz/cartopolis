from . import db
import logging as lg
import json

class Islands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Integer, nullable=False)
    y = db.Column(db.Integer, nullable=False)
    isaland_type = db.Column(db.Integer, nullable=False)
    available_town = db.Column(db.Integer, nullable=False)

    def __init__(self, id, x, y, isaland_type, available_town):
        self.id = id
        self.x = x
        self.y = y
        self.isaland_type = isaland_type
        self.available_town = available_town

class Towns(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    island_x = db.Column(db.Integer, nullable=False)
    island_y = db.Column(db.Integer, nullable=False)
    number_on_island = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)

    def __init__(self, id, player_id, name, island_x, island_y, number_on_island, points):
        self.id = id
        self.player_id = player_id
        self.name = name
        self.island_x = island_x
        self.island_y = island_y
        self.number_on_island = number_on_island
        self.points = points

class Alliances(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    villages = db.Column(db.Integer, nullable=False)
    members = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, points, villages, members, rank):
        self.id = id
        self.name = name
        self.points = points
        self.villages = villages
        self.members = members
        self.rank = rank

class Players(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    alliance_id = db.Column(db.Integer, nullable=False)
    points = db.Column(db.Integer, nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    towns = db.Column(db.Integer, nullable=False)

    def __init__(self, id, name, alliance_id, points, rank, towns):
        self.id = id
        self.name = name
        self.alliance_id = alliance_id
        self.points = points
        self.rank = rank
        self.towns = towns

def init_db():
    db.drop_all()
    db.create_all()
    lg.warning('database init')