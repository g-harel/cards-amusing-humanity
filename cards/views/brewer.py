import logging
import random
from datasource.database import db
from models.answers import Answer, row2dict
from models.questions import Question, row2dict

# Helper function in charge of getting X random answers card
def get_random_answer(number_of_item, deck):
    """Obtain X number of random answers from database with deck"""
    random_answers = []
    try:
        number_of_item_int = int(number_of_item)
        total_cards = db.session.query(Answer).filter(Answer.deck == deck)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)

        if(deck.__len__() == 0):
            return

        while random_answers.__len__() < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_answers.__contains__(row):
                random_answers.append(row)

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


def get_random_question(number_of_item, deck):
    """Obtain X number of questions from database with the deck"""
    random_questions = []
    try:
        number_of_item_int = int(number_of_item)
        total_cards = db.session.query(Question).filter(Question.deck == deck)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)

        if(deck.__len__() == 0):
            return
        while random_questions.__len__() < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_questions.__contains__(row):
                random_questions.append(row)

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