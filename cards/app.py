from flask import Flask
from views import answers, questions, card_brewer, main
from settings import DatabaseConfig
from datasource.database import db
from waitress import serve

application = Flask(__name__)

def create_app():

    conf = DatabaseConfig()
    application.config['DEBUG'] = True
    application.config['SQLALCHEMY_DATABASE_URI'] = conf.get_db_uri()
    db.init_app(application)
    application.register_blueprint(answers.ans)
    application.register_blueprint(questions.ques)
    application.register_blueprint(card_brewer.brew)
    application.register_blueprint(main.main)
    return application


if __name__ == '__main__':
    application = create_app()
    serve(application, host='0.0.0.0', port=8000)
