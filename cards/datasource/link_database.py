from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from settings import DatabaseConfig


"""Initialize a database"""
db_uri = DatabaseConfig().get_db_uri()
engine = create_engine(db_uri, convert_unicode=True, echo=True)
db_session = scoped_session(sessionmaker(
    autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    import models.answers, models.questions
    Base.metadata.create_all(bind=engine)