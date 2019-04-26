import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Records table contains all submitted game data.
# Game outcomes are recorded as a 3-tuple containing the question, the selected answer and one of the non-selected answers.
# This means each game of with N possible answers will be stored as N rows in the table.
# Using this scheme, we can reuse results from similar games without requiring the exact same cards.
class Record(Base):
    __tablename__ = "records"

    # Primary key is never used, but is required for SQLAlchemy's mapper.
    id = Column(Integer, primary_key=True)

    question = Column(String(), nullable=False)
    selected_answer = Column(String(), nullable=False)
    other_answer = Column(String(), nullable=False)


class RecordStore():
    db = None

    def __init__(self, app):
        # Postgres config used to connect to analytics database.
        POSTGRES = {
            "db": os.getenv("POSTGRES_DB", default=""),
            "user": os.getenv("POSTGRES_USER", default=""),
            "pass": os.getenv("POSTGRES_PASSWORD", default=""),
            "host": "analytics-postgres",
            "port": "5432",
        }

        # Configure app before handing over the instance to SQLAlchemy.
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = \
            "postgresql://%(user)s:%(pass)s@%(host)s:%(port)s/%(db)s" % POSTGRES

        # Create a database "client".
        self.db = SQLAlchemy(app)

    # Reset the database contents.
    def reset(self):
        Base.metadata.drop_all(bind=self.db.engine)
        Base.metadata.create_all(bind=self.db.engine)

    # Add a new record to the database.
    def add(self, question, choice, other_answer):
        self.db.session.add(Record(question=question, selected_answer=choice, other_answer=other_answer))
        self.db.session.commit()

    # Count records that agree with the choice.
    def count_agree(self, question, choice, answers):
        return self.db.session.query(Record) \
            .filter_by(question=question) \
            .filter_by(selected_answer=choice) \
            .filter(Record.other_answer.in_(answer["id"] for answer in answers)) \
            .count()

    # Count records that disagree with the choice.
    def count_disagree(self, question, choice, answers):
        return self.db.session.query(Record) \
            .filter_by(question=question) \
            .filter(Record.selected_answer.in_(answer["id"] for answer in answers)) \
            .filter_by(other_answer=choice) \
            .count()

