from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

with app.app_context():
    # Importer les modèles ici pour éviter les importations circulaires
    from . import models
    db.create_all()

from . import views

@app.cli.command('init_db')
def init_db():
    models.init_db()