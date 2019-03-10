from .raw_data_parser import ParseRawData
from .database_conn_factory import DatabaseFactory
from .reset_database import ResetDatabase


class FillDatabase:
    MAX_NUMBER_OF_ANSWERS = 1000
    MAX_NUMBER_OF_QUESTIONS = 100
    __INSERT_QUERY_QUESTIONS = "INSERT INTO questions (id, text, extension) VALUES(%s, %s, %s)"
    __INSERT_QUERY_ANSWERS = "INSERT INTO answers (id, text, extension) VALUES(%s, %s, %s)"

    def __init__(self, max_number_of_answers=MAX_NUMBER_OF_ANSWERS,
                 max_num_questions=MAX_NUMBER_OF_QUESTIONS):
        """Allow to setup the table length"""
        self.MAX_NUMBER_OF_QUESTIONS = max_num_questions
        self.MAX_NUMBER_OF_ANSWERS = max_number_of_answers

    def fill_db(self):
        parser = ParseRawData()
        data = parser.parse_cards_json()
        print("*** Filling answers table ***")
        formatted_answers = parser.parse_answers(data)
        if formatted_answers.__len__() > self.MAX_NUMBER_OF_ANSWERS:
            formatted_answers = formatted_answers[:self.MAX_NUMBER_OF_ANSWERS]

        print("*** Filling questions table ***")
        formatted_questions = parser.parse_questions(data)
        if formatted_questions.__len__() > self.MAX_NUMBER_OF_QUESTIONS:
            formatted_questions = formatted_questions[:self.MAX_NUMBER_OF_QUESTIONS]

        # Clean answer & Question tables
        resetter = ResetDatabase().clean_tables()

        # Insert all answers
        for i, row in enumerate(formatted_answers):
            self.insert_answer_row(row)

        for i, row in enumerate(formatted_questions):
            self.insert_question_row(row)

        print("TABLES FILLED")

    def insert_answer_row(self, row):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__INSERT_QUERY_ANSWERS, (row['id'], row['text'], row['extension']))
            connection.commit()
        except Exception as error:
            print("Problem inserting in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()

    def insert_question_row(self, row):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__INSERT_QUERY_QUESTIONS, (row['id'], row['text'], row['extension']))
            connection.commit()
        except Exception as error:
            print("Problem inserting in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()







