import os

# # Postgres config used to connect to cards database.
# POSTGRES = {
#     "db": os.environ["POSTGRES_DB"],
#     "user": os.environ["POSTGRES_USER"],
#     "pass": os.environ["POSTGRES_PASSWORD"],
#     "host": "cards-postgres",
#     "port": "5432",
# }

# Postgres config used to connect to cards database for local dev
POSTGRES = {
    "db": '',
    "user": 'postgres',
    "pass": '',
    "host": "localhost",
    "port": "5432",
}

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
        db = {}
        try:
            db['user'] = POSTGRES['user']
            db['pw'] = POSTGRES['pass']
            db['host'] = POSTGRES['host']
            db['port'] = POSTGRES['port']
            db['db'] = POSTGRES['db']

        except Exception as error:
            print("Can't grab database configuration file " )
            print(error)
        return db

    def get_db_uri(self):
        """Read from configuration file database.ini"""
        db_config = self.grab_configuration()
        db_uri = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % db_config
        print(db_uri)
        return db_uri
