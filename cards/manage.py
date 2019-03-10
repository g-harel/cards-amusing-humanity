from datasource.reset_database import  ResetDatabase
from datasource.init_database import init_db
from datasource.fill_database import FillDatabase


def recreate_db():
    resetter = ResetDatabase()
    try:
        resetter.drop_all()
        init_db()
    except Exception as error:
        print("Can't reset database")
        print(error)

    filler = FillDatabase()
    try:
        filler.fill_db()
    except Exception as error:
        print("Can't fill database")
        print(error)

    print("!!!!! Database Rebuild !!!!")



