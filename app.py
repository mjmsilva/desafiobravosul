from datetime import datetime, timedelta
from flask import Flask, jsonify
from flask_restful import Resource, Api
from models import Book, Rent, db_session

app = Flask(__name__)
api = Api(app)

#Define qual o status do livro
def checkStatus(book):
    if book.reserved == True:
        book.status = 'emprestado'
    else:
        book.status = 'disponivel'

#Aplica a multa conforme a regra ( valor da multa = 1)
def checkPastDue(book):
    dateRent = book.dateRent
    today = datetime.now()
    delta = today - dateRent
    print(delta.days)
    if 0 <= delta.days <= 3:
        book.fine = 0
    elif 3 <= delta.days <= 6:
        book.fine = 1 + 1 * 0.03 + 1 * (delta.days * 0.02)
    elif 6 < delta.days < 8:
        book.fine = 1 + 1 * 0.05 + 1 * (delta.days * 0.04)
    elif delta.days >= 8:
        book.fine = 1 + 1 * 0.07 + 1 * (delta.days * 0.06)

#lista livros conforme o solicitado
def listBooks(books):
    response = []
    for book in books:
        checkStatus(book)
        checkPastDue(book)
        tempbook = {
            'id': book.id,
            'Titulo': book.title,
            'reservado': book.reserved,
            'status': book.status,
            'data': book.dateRent,
            'multa': book.fine
        }
        response.append(tempbook)

    return jsonify(response)

#Retornar todos livros
class Books(Resource):
    def get(self):
        books = Book.query.all()
        return listBooks(books)

#Lista de livros emprestados
class RentedBooks(Resource):
    def get(self, id):
        books = db_session.query(Book).join(Rent).filter(Rent.client_id==id)
        if not hasattr(books.first(), 'id'):
            return "Cliente sem reservas."
        return listBooks(books)

#Reserva de livro
class ReserveBook(Resource):
    def get(self, id):
        books = Rent.query.filter_by(book_id=id)
        existBook = Book.query.filter_by(id=id).first()

        if not hasattr(existBook, 'id'):
            return "Livro não encontrado."

        response = []
        for book in books:
            tempbook = {
                'id': book.id,
                'dateReservation': book.dateReservation
            }
            response.append(tempbook)

        reservedBook = [b['dateReservation'] for b in response]
        if not reservedBook: #Se livro ainda não foi reservado
            newDate = datetime.now() + timedelta(days=3)
            newReserve = Rent(book_id=id, dateReservation=newDate)
            newReserve.save()
            msg = "Reservado de: " + datetime.now().strftime('%d-%b-%y') + " a " + newDate.strftime('%d-%b-%y')
            return msg
        else: #se livro está reservado verifica se já foi entregue para definir a data da reserva
            lastDate = max(reservedBook)
            print(lastDate)
            if lastDate <= datetime.now():
                newDate = datetime.now() + timedelta(days=3)
                newReserve = Rent(book_id=id, dateReservation=newDate)
                newReserve.save()
                msg = "Reservado de: " + datetime.now().strftime('%d-%b-%y') + " a " + newDate.strftime('%d-%b-%y')
            else:
                newDate = lastDate + timedelta(days=3)
                newReserve = Rent(book_id=id, dateReservation=newDate)
                newReserve.save()
                msg = "Reservado de: " + lastDate.strftime('%d-%b-%y') + " a " + newDate.strftime('%d-%b-%y')

            existBook.reserved = True
            existBook.save()
            return msg

api.add_resource(Books, '/books')
api.add_resource(RentedBooks, '/client/<int:id>/books')
api.add_resource(ReserveBook, '/books/<int:id>/reserve')

if __name__ == '__main__':
    app.run(debug=True)
