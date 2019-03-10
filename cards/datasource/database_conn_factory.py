import psycopg2
from settings import DatabaseConfig


class DatabaseFactory:
    conn = None

    def get_manual_connection(self):
        """Obtain manual DB connection"""
        try:
            conf = DatabaseConfig()
            connection_uri = conf.get_db_uri()
            self.conn = psycopg2.connect(connection_uri)
            return self.conn
        except Exception as error:
            print('problem while getting manual connection')
            print(error)
            raise error

    def close_manual_connection(self):
        """Close manual connection"""
        try:
            if self.conn is not None:
                self.conn.close()
        except Exception as error:
            print("can't close connection")
            print(error)
            raise error

