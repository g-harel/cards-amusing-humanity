from .database_conn_factory import DatabaseFactory


class ResetDatabase:
    __DELETE_ALL_FROM_ANSWERS = "DELETE FROM answers"
    __DELETE_ALL_FROM_QUESTIONS = "DELETE FROM questions"
    __DELETE_ALL_FROM_HISTORY ="DELETE FROM history"
    __DROP_ALL = 'DROP SCHEMA public CASCADE;'
    __REBUILD_SCHEMA = 'CREATE SCHEMA public;'

    def clean_answers_table(self):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__DELETE_ALL_FROM_ANSWERS)
            connection.commit()
        except Exception as error:
            print("Problem cleaning in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()

    def clean_questions_table(self):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__DELETE_ALL_FROM_QUESTIONS)
            connection.commit()
        except Exception as error:
            print("Problem cleaning in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()

    def clean_history_table(self):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__DELETE_ALL_FROM_HISTORY)
            connection.commit()
        except Exception as error:
            print("Problem cleaning in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()

    def clean_tables(self):
        self.clean_history_table()
        self.clean_answers_table()
        self.clean_questions_table()

    def drop_all(self):
        conn_factory = DatabaseFactory()
        cursor = None
        try:
            connection = conn_factory.get_manual_connection()
            cursor = connection.cursor()
            cursor.execute(self.__DROP_ALL)
            cursor.execute(self.__REBUILD_SCHEMA)
            connection.commit()
        except Exception as error:
            print("Problem cleaning in table")
            print(error)
            raise error
        finally:
            if cursor is not None:
                cursor.close()
        conn_factory.close_manual_connection()