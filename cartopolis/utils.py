from cartopolis.models import Islands, Towns, Players, Alliances
from sqlalchemy import or_, and_, not_, func
import logging
from . import db

def getTopAlliances():
    return Alliances.query.filter(Alliances.rank < 20).order_by(Alliances.rank.asc()).limit(20).all()

def getIslandCentral():
    return Islands.query.filter(Islands.x.between(400, 600), Islands.y.between(400, 600), or_(Islands.isaland_type < 17, Islands.isaland_type > 36)).all()

def getTownsCentral():
    # Exemple de conditions
    condition_1 = Towns.island_x == Islands.x
    condition_2 = Towns.island_y == Islands.y

    # Requête avec inner join et deux conditions
    towns = db.session.query(Towns, Islands, Players, Alliances).filter(Towns.island_x.between(400, 600), Towns.island_y.between(400, 600)).join( Islands, and_(condition_1, condition_2)).join( Players, and_(Towns.player_id == Players.id)).outerjoin( Alliances, and_(Players.alliance_id == Alliances.id)).all()
    return towns

def getOuterIsland():
    return Islands.query.filter(or_(Islands.x.between(200, 400), Islands.x.between(600, 800)), or_(Islands.y.between(200, 400), Islands.y.between(600, 800)), or_(Islands.isaland_type < 17, Islands.isaland_type > 36)).all()

def getOuterTowns():
   
    condition_1 = Towns.island_x == Islands.x
    condition_2 = Towns.island_y == Islands.y

    towns = db.session.query(Towns, Islands, Players, Alliances).filter(
        and_(
            func.pow(Towns.island_x - 500, 2) + func.pow(Towns.island_y - 500, 2) <= func.pow(275, 2),


            not_(and_( Towns.island_x.between(400, 600), Towns.island_y.between(400, 600)))
        )
        ).join( 
            Islands, and_(condition_1, condition_2)
        ).join( 
            Players, and_(Towns.player_id == Players.id)
        ).join( 
            Alliances, and_(Players.alliance_id == Alliances.id)
        ).all()
    
    return towns


def serialize_island(island):
    return {
        'id': island.id,
        'x': island.x,
        'y': island.y,
        'isaland_type': island.isaland_type
    }


def serialize_alliance(alliance):
    logging.warning(alliance.name)
    return {
        'id': alliance.id,
        'name':alliance.name,
        'rank': alliance.rank,
        'points': alliance.points,
        'members': alliance.members
    }

def serialize_town(town, island, player, alliance):
    data = {
        'id': town.id,
        'island_x': town.island_x,
        'island_y': town.island_y,
        'player_id': town.player_id,
        'points' : town.points,
        'number_on_island': town.number_on_island,
        'name': town.name,
        'isaland_type' : island.isaland_type,
        'player_id': player.id,
        'player_name': player.name,
    }

    if(alliance):
        data_ally = {
            'alliance_id': alliance.id,
            'alliance_name': alliance.name
        }

        data.update(data_ally)
    
    
    return data