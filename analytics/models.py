from app import db

class Record(db.Model):
    __tablename__ = "records"

    question = db.Column(db.String(), nullable=False)
    selected_answer = db.Column(db.String(), nullable=False)
    other_answer = db.Column(db.String(), nullable=False)
