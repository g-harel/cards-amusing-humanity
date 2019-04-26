from memory.storage import Storage
from datasource.database import db
from models.answers import Answer
from models.questions import Question


class PStorage(Storage):
    """ This class is allowing testing by decoupling db from views"""

    def answers_for_deck(self, deck):
        data = None
        try:
            data = db.session.query(Answer).filter(Answer.deck == deck)
            db.session.close()
            return data
        except Exception as error:
            print(error)
            db.session.close()
            return data

    def questions_for_deck(self, deck):
        data = None
        try:
            data =  db.session.query(Question).filter(Question.deck == deck)
            db.session.close()
            return data
        except Exception as error:
            print(error)
            db.session.close()
            return data
