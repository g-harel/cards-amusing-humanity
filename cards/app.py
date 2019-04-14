from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from views import  general, game
from settings import DatabaseConfig
from datasource.database import db
from datasource.database_rebuild import DatabaseRebuilder

# Token expiry in minutes.
# Value is used to clear the token blacklist.
# exp = 60 * int(float(os.getenv("TOKEN_TTL_HOURS")))
exp = 60 * int(float(1))

def create_app():
    
    app = Flask(__name__)
    conf = DatabaseConfig()
    app.config['DEBUG'] = False
    # Configure app before handing over the instance to SQLAlchemy.
    app.config["SQLALCHEMY_DATABASE_URI"] = conf.get_db_uri()
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Init Database
    db.init_app(app)

    # Rebuild or build the database
    db.drop_all()
    db.create_all()
    rebuilder = DatabaseRebuilder()
    rebuilder.rebuild()

    app.register_blueprint(game.game)
    app.register_blueprint(general.main)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0")