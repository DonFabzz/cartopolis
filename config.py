import os

URL_ISLANDS = "http://fr166.grepolis.com/data/islands.txt.gz"
URL_TOWNS = "http://fr166.grepolis.com/data/towns.txt.gz"
URL_PLAYERS = "http://fr166.grepolis.com/data/players.txt.gz"
URL_ALLIANCES = "http://fr166.grepolis.com/data/alliances.txt.gz"

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')