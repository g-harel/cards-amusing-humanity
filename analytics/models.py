from app import db

# Records table contains all submitted game data.
# Game outcomes are recorded as a 3-tuple containing the question, the selected answer and one of the non-selected answers.
# This means each game of with N possible answers will be stored as N rows in the table.
# Using this scheme, we can reuse results from similar games without requiring the exact same cards.
#   ex.
#       Q | A1 A2 A3 => A1 selected => for Q :: [A1 > A2] and [A1 > A3]
#       Q | A1 A2 A4 => We can reuse the fact that [A1 > A2] even if the third answer has changed.
class Record(db.Model):
    __tablename__ = "records"

    question = db.Column(db.String(), nullable=False)
    selected_answer = db.Column(db.String(), nullable=False)
    other_answer = db.Column(db.String(), nullable=False)
