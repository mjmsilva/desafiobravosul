from sqlalchemy import create_engine, Column, INTEGER, String, DATETIME, BOOLEAN, FLOAT, ForeignKey
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///bookstore.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

class Book(Base):
    __tablename__ = 'book'
    id = Column(INTEGER, primary_key=True)
    title = Column(String(256), index=True)
    status = Column(String(20))
    reserved = Column(BOOLEAN)
    fine = Column(FLOAT)
    dateRent = Column(DATETIME)

    def __repr__(self):
        return '<Book {}>'.format(self.id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Client(Base):
    __tablename__ = 'client'
    id = Column(INTEGER, primary_key=True)
    name = Column(String(256), index=True)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

class Rent(Base):
    __tablename__ = 'rent'
    id = Column(INTEGER, primary_key=True)
    client_id = Column(INTEGER)
    book_id = Column(INTEGER, ForeignKey('book.id'))
    book = relationship('Book')
    dateReservation = Column(DATETIME)

    def __repr__(self):
        return '<Rent {}>'.format(self.book_id, self.client_id)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == '__main__':
    init_db()
