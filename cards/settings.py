from dotenv import load_dotenv
import os


class DatabaseConfig:
    """ Configuration of Database"""
    DEFAULT_CONF_FILE_NAME = '.env'
    DEFAULT_DB_SECTION = 'postgresql'

    def __init__(self, configuration_file_name=DEFAULT_CONF_FILE_NAME, section=DEFAULT_DB_SECTION):
        self.file_name = configuration_file_name
        self.section = section

    @staticmethod
    def grab_configuration():
        """Grab data from database.int"""
        load_dotenv()
        db = {}
        try:
            db['user'] = os.getenv('DB_USER')
            db['pw'] = os.getenv('DB_PWD')
            db['host'] = os.getenv('DB_HOST')
            db['port'] = os.getenv('DB_PORT')
            db['db'] = os.getenv('DB_NAME')
        except Exception as error:
            print("Can't grab database configuration file " )
            print(error)
        return db

    def get_db_uri(self):
        """Read from configuration file database.ini"""
        db_config = self.grab_configuration()
        db_uri = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % db_config
        return db_uri
