from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import  general, game
from settings import DatabaseConfig
from datasource.database import db
from datasource.database_rebuild import DatabaseRebuilder


def create_app():
    """ Helper Method to setup application """    
    app = Flask(__name__)
    conf = DatabaseConfig()
    app.config['DEBUG'] = False
    app.config["JSON_SORT_KEYS"] = False
    # Configure app before handing over the instance to SQLAlchemy.
    app.config["SQLALCHEMY_DATABASE_URI"] = conf.get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Init Database
    db.init_app(app)
    app.register_blueprint(game.game)
    app.register_blueprint(general.main)
    return app


if __name__ == '__main__':
    app = create_app()
    # Rebuild or build the database
    rebuilder = DatabaseRebuilder()
    rebuilder.rebuild(app)
    app.run(host="0.0.0.0")