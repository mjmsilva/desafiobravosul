from models import Book, Client, Rent
from datetime import datetime

def insertRent():
    rent = Rent(client_id=1, book_id=1, dateReservation=datetime(2020, 10, 11))
    rent.save()
    rent1 = Rent(client_id=1, book_id=2, dateReservation=datetime(2020, 10, 11))
    rent1.save()
    rent2 = Rent(client_id=1, book_id=3, dateReservation=datetime(2020, 10, 11))
    rent2.save()

def insertBook():
    book = Book(title='Harry Potter', reserved=False, dateRent=datetime(2020, 10, 13))
    book.save()
    book1 = Book(title='Game of thrones', reserved=False, dateRent=datetime(2020, 10, 11))
    book1.save()
    book2 = Book(title='Rangers', reserved=False, dateRent=datetime(2020, 10, 12))
    book2.save()
    book3 = Book(title='Lord of the rings', reserved=False, dateRent=datetime(2020, 9, 11))
    book3.save()
    book4 = Book(title='Treasure island', reserved=False, dateRent=datetime(2020, 10, 5))
    book4.save()

def insertClient():
    client = Client(name="Cliente 1")
    client.save()
    client1 = Client(name="Cliente 2")
    client1.save()
    client2 = Client(name="Cliente 3")
    client2.save()

def deleteBooks():
    books = Book.query.all()
    for b in books:
        b.delete()

def deleteRent():
    rents = Rent.query.all()
    for r in rents:
        r.delete()

def queryBook():
    books = Book.query.all()
    print(books)

def queryBook():
    rents = Rent.query.all()
    print(rents)

if __name__=='__main__':
    #deleteRent()
    #queryBook()
    #deleteBooks()
    #query()
    insertRent()
    insertBook()
    insertClient()
