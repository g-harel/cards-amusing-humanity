import json
from util.uuid_generator import UuidGenerator

class ParseRawData:
    DEFAULT_DATA_PATH = './resources/cards.json'

    def __init__(self, raw_data_path=DEFAULT_DATA_PATH):
        self.DEFAULT_DATA_PATH = raw_data_path


    @staticmethod
    def parse_cards_json(path_to_json=DEFAULT_DATA_PATH):
        """Grab data from path"""
        data_dict = {}
        try:
            with open(path_to_json) as file:
                data_dict = json.load(file)
        except Exception as error:
            print("Not able to load file")
            print(error)

        return data_dict

    def parse_questions(self, data_dict):
        all_questions = []
        for i, row in enumerate(data_dict):
            if row['cardType'] == 'Q' and row['numAnswers'] == 1:
                db_row = {'id': UuidGenerator().generate_uuid(),
                          'text': row['text'],
                          'extension': row['expansion']}
                all_questions.append(db_row)
        print(all_questions.__len__())
        return all_questions

    def parse_answers(self, data_dict):
        all_answers = []
        for i, row in enumerate(data_dict):
            if row['cardType'] == "A":
                db_row = {'id': UuidGenerator().generate_uuid(),
                          'text': row['text'],
                          'extension': row['expansion']}
                all_answers.append(db_row)
        print(all_answers.__len__())
        return all_answers


