from datasource.database import db
import random
from models.answers import Answer, row2dict
from models.questions import Question, row2dict

# Helper function in charge of getting X random answers card
def get_random_answer(number_of_item, extension):
    """Obtain X number of random answers from database with deck"""
    random_answers = []
    try:
        number_of_item_int = int(number_of_item)
        counter = 0
        total_cards = db.session.query(Answer).filter(Answer.extension == extension)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)
        
        if(deck.__len__() == 0):
            return
   
        while counter < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_answers.__contains__(row):
                random_answers.append(row)
                counter = counter + 1

        db.session.close()
        return [row2dict(answer) for answer in random_answers]
    except ValueError:
        return ValueError
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return Exception

    finally:
        db.session.close()


def get_random_question(number_of_item, extension):
    """Obtain X number of questions from database with the deck"""
    random_questions = []
    try:
        number_of_item_int = int(number_of_item)
        counter = 0
        total_cards = db.session.query(Question).filter(Question.extension == extension)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)
        
        if(deck.__len__() == 0):
            return
        while counter < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_questions.__contains__(row):
                random_questions.append(row)
                counter = counter + 1

        db.session.close()
        return [row2dict(question) for question in random_questions]
    except ValueError:
        return ValueError
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return Exception

    finally:
        db.session.close()