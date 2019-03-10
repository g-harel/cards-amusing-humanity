from sqlalchemy import Column, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from datasource.init_database import Base
from sqlalchemy.orm import relationship


def row2dict(row):
    """Convert SQL row to text"""
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class History(Base):
    """ Answer cards"""
    __tablename__ = "history"
    id = Column(UUID(as_uuid=True), primary_key=True)
    card_id = Column(UUID(as_uuid=True), ForeignKey('questions.id'))
    card_id_rel = relationship("Question")
    text_sent = Column(Text, nullable=False)
    time_sent = Column(Text, nullable=False)

    def __repr__(self):
        return '<Question-History {}>'.format(self.card_id)
