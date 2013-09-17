---
title: 'Many to Many Relationship in Sqlalchemy'
layout: post
tags:
    - python
    - sqlalchemy
---

There are three key words of Many-to-Many: 'primaryjoin', 'secondary', 'secondaryjoin'. And they are three parameters of funtion ‘Relationship’.

In SQL, to impletement Many=to-Many requires three tables. Table A and B for two entities need to be related, and table C present the relationship. Parameter 'secondary' is the table C, 'primaryjoin' is the method that connectC and A (or B), 'secondaryjoin' is another method that connect C and B (or A).

For instance, the [code]() may look like this:

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
