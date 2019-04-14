import json
import os
from datasource.database import db
from models.answers import Answer, row2dict
from models.questions import Question, row2dict
from datasource.link_database import init_db


class DatabaseRebuilder:
    """ Rebuilding database from resource folder """
    DEFAULT_ANSWERS_JSON = '/../resources/postgres_public_answers.json'
    DEFAULT_QUESTIONS_JSON = '/../resources/postgres_public_questions.json'
    def rebuild(self, app, forceRebuild=False):
         with app.app_context():
            """ Only Rebuild database if we need to """
            number_of_answer  = 0
            number_of_question = 0

            try:
                number_of_answer = db.session.query(Answer).count()
            except Exception as error:
                # print(error)
                print("Can't grab number of answers")
            finally:
                db.session.close()
            try:
                number_of_question = db.session.query(Question).count()
            except Exception as error:
                # print(error)
                print("Can't grab number of answers")
            finally:
                db.session.close()

            if(number_of_answer > 0 and number_of_question > 0 and not forceRebuild):
                print("...Database is ready...")
                return
        
            print("............ Rebuilding database..............")
            if(forceRebuild):
                try:
                    db.session.query(Question).delete()
                    db.session.query(Answer).delete()
                    db.session.commit()
                    db.session.close()
                except:
                    db.session.rollback()
                    print("Problem while cleaning db")
            
            # Init db, build table if they are not there
            init_db()

            if(number_of_answer == 0):
               self.rebuild_answers_table()
            
            if(number_of_question == 0):
                self.rebuild_questions_table()

            return

    def rebuild_answers_table(self):
        """ Rebuilding Answer Table """
        anwers = self.grab_json(self.DEFAULT_ANSWERS_JSON)
        # Convert answers Dict to Answer and save in db
        Answers = []
        for i, row in enumerate(anwers):
            Answers.append(Answer(
                id=row['id'],
                text=row['text'],
                extension=row['extension']))
        try:
            db.session.add_all(Answers)
            db.session.commit()
            db.session.close()
        except Exception as error:
            print("Problem while saving all answers")
            print(error)


    def rebuild_questions_table(self):
        """ Rebuilding Questions Table """
        questions = self.grab_json(self.DEFAULT_QUESTIONS_JSON)
        # Convert questions dict to Question and save in db 
        Questions = []
        for i, row in enumerate(questions):
            Questions.append(Question(
                id=row['id'],
                text=row['text'],
                extension=row['extension']))
        try:
            db.session.add_all(Questions)
            db.session.commit()
            db.session.close()
        except Exception as error:
            print("Problem while saving all answers")
            print(error)


    def grab_json(self, path_to_json):
        """ Grab data from json """
        data_dict = {}
        direc = os.path.dirname(os.path.realpath(__file__))
        absolute = direc + path_to_json
        try:
            with open(absolute) as file:
                data_dict = json.load(file)
                file.close()
        except Exception as error:
            print("Problem with grab_json")
            print(error)
        
        return data_dict

           