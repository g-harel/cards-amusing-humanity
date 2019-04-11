from app import db

class test(db.Model):
    __tablename__ = "test"
    test = db.Column(db.String(), nullable=False)
