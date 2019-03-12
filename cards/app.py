from flask import Flask
from views import answers, questions, card_brewer, main
from settings import DatabaseConfig
from datasource.database import db


def create_app():
    app = Flask(__name__)
    conf = DatabaseConfig()
    app.config['DEBUG'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = conf.get_db_uri()
    db.init_app(app)
    app.register_blueprint(answers.ans)
    app.register_blueprint(questions.ques)
    app.register_blueprint(card_brewer.brew)
    app.register_blueprint(main.main)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
