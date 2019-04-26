from memory.storage import Storage


def test_brewer_answers():
    """ Testing the logic of the brewer with a fake database """
    from views.brewer import get_random_answer
    fake_db = FakeCardsDatabase()
    number_of_cards = 2
    random_answers = get_random_answer(number_of_cards, 'special', fake_db, True)
    assert random_answers.__len__() == number_of_cards


def test_brewer_questions():
    """ Testing the logic of the brewer with a fake database """
    from views.brewer import get_random_question
    fake_db = FakeCardsDatabase()
    number_of_cards = 3
    random_questions = get_random_question(number_of_cards, 'special', fake_db, True)
    assert random_questions.__len__() == number_of_cards


def test_brewer_answers_wrong_deck():
    """ Testing the logic of the brewer with a fake database """
    from views.brewer import get_random_answer
    fake_db = FakeCardsDatabase()
    number_of_cards = 2
    random_answers = get_random_answer(number_of_cards, 'wrong', fake_db, True)
    assert random_answers is None


class FakeCardsDatabase(Storage):

    def answers_for_deck(self, deck):
        answers = []
        answers.append({'id': '19021ek', 'text': 'dodo', 'deck': 'special'})
        answers.append({'id': 'w33rr2', 'text': 'Bob', 'deck': 'special'})
        answers.append({'id': '9012k3e3', 'text': 'Micheal Scott', 'deck': 'special'})
        answers.append({'id': '23k09kd', 'text': 'Jacque', 'deck': 'special'})

        answers.append({'id': '9ij9dj', 'text': 'Spider-man', 'deck': 'foo'})
        answers.append({'id': 'dk903dk', 'text': 'Foobar', 'deck': 'foo'})
        filtered_deck = []
        for i, row in enumerate(answers):
            if row['deck'] == deck:
                filtered_deck.append(row)

        return filtered_deck

    def questions_for_deck(self, deck):
        questions = []
        questions.append({'id': 'som2309k', 'text': ' ___ is the best topping on a pizza', 'deck': 'special'})
        questions.append({'id': '9012k1s', 'text': ' ___ is the best car', 'deck': 'special'})
        questions.append({'id': '902dk0d9kd', 'text': ' ___ is the best bob', 'deck': 'special'})
        questions.append({'id': '0d9qjd0qdqw', 'text': ' ___ is the worst human', 'deck': 'special'})

        questions.append({'id': '29dkda', 'text': ' Python is good as a ____ ', 'deck': 'foo'})
        questions.append({'id': '2e90d0kw0k', 'text': ' ___ is the color of hell ', 'deck': 'foo'})
        filtered_deck = []
        for i, row in enumerate(questions):
            if row['deck'] == deck:
                filtered_deck.append(row)

        return filtered_deck
