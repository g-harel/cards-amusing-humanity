import random
import json


# Helper function in charge of getting X random answers card
def get_random_answer(number_of_item, deck, storage_inst, testing):
    """Obtain X number of random answers from database with deck"""
    random_answers = []
    try:
        number_of_item_int = int(number_of_item)
        total_cards = storage_inst.answers_for_deck(deck)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)

        if deck.__len__() == 0:
            return

        while random_answers.__len__() < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_answers.__contains__(row):
                random_answers.append(row)
        if testing:
            return [row2dict_testing(answer) for answer in random_answers]

        return [row2dict(answer) for answer in random_answers]
    except ValueError:
        return ValueError
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return Exception


def get_random_question(number_of_item, deck, storage_inst, testing):
    """Obtain X number of questions from database with the deck"""
    random_questions = []
    try:
        number_of_item_int = int(number_of_item)
        total_cards = storage_inst.questions_for_deck(deck)
        deck = []

        for i, data in enumerate(total_cards):
            deck.append(data)

        if deck.__len__() == 0:
            return
        while random_questions.__len__() < number_of_item_int:
            random_index = random.randrange(0, deck.__len__())
            row = deck[random_index]
            # Making sure data are unique and it's the right deck
            if not random_questions.__contains__(row):
                random_questions.append(row)

        if testing:
            return [row2dict_testing(question) for question in random_questions]

        return [row2dict(question) for question in random_questions]
    except ValueError:
        return ValueError
    except Exception as error:
        print("Problem while getting random answers")
        print(error)
        return Exception


def row2dict(row):
    """Convert SQL row to text"""
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


def row2dict_testing(row):
    return str(json.dumps(row))
