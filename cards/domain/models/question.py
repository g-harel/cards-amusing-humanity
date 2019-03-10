from sqlalchemy import Column, Text, String
from sqlalchemy.dialects.postgresql import UUID
from datasource.init_database import Base


def row2dict(row):
    """Convert SQL row to text"""
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class Question(Base):
    """ Answer cards"""
    __tablename__ = "questions"
    id = Column(UUID(as_uuid=True), primary_key=True)
    text = Column(Text, nullable=False)
    extension = Column(String(100), nullable=False)

    def __repr__(self):
        return '<Question-Card {}>'.format(self.text)
