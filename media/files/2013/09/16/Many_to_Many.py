from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

attend_party = Table('attend_party',
    Column('people_id', Integer, ForeignKey('people.id')),
    Column('party_id', Integer, ForeignKey('party.id'))
)

class People(Base):
    __tablename__ = 'people'

    id = Column(
        Integer, primary_key=True
    )


class Party(Base):
    __tablename__ = 'party'

    id = Column(Integer, primary_key=True)

    participant = relationship(
        'People',
        primaryjoin= lambda : Party.id==attend_party.c.party_id,
        secondary=attend_party,
        secondaryjoin= lambda : attend_party.c.people_id==People.id,
        backref=backref('parties_attended')
    )