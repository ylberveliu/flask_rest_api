from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, Schema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    pages = db.Column(db.Integer, nullable=False)

    def __init__(self, title, author, year, pages):
        self.title = title
        self.author = author
        self.year = year
        self.pages = pages

    def __repr__(self):
        return '<Book %s>' % self.title


class BookSchema(Schema):
    class Meta:
        fields = ('title', 'author', 'year', 'pages')


book_schema = BookSchema()
books_schema = BookSchema(many=True)


@app.route('/api/v1/resources/books', methods=['GET'])
def index():
    results = []
    if 'title' in request.args:
        search = "%{}%".format(request.args['title'])
        results = Book.query.filter(Book.title.like(search)).all()
    else:
        results = Book.query.all()

    if len(results):
        return jsonify(books_schema.dump(results))
    else:
        return "0 books", 404


@app.route('/api/v1/resources/books', methods=['POST'])
def store():
    title = request.json['title']
    author = request.json['author']
    year = request.json['year']
    pages = request.json['pages']

    book = Book(title, author, year, pages)
    db.session.add(book)
    db.session.commit()

    return book_schema.jsonify(book), 201


@app.route('/api/v1/resources/books/<int:book_id>', methods=['PUT'])
def update(book_id):
    book = Book.query.get_or_404(book_id)
    # if 'title' in request.json:
    #     title = request.json['title']
    book.title = request.json['title']
    book.author = request.json['author']
    book.year = request.json['year']
    book.pages = request.json['pages']

    db.session.commit()

    return book_schema.jsonify(book)


@app.route('/api/v1/resources/books/<int:book_id>', methods=['DELETE'])
def delete(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    # return book_schema.jsonify(book)
    return jsonify({'status': 'Book was deleted successfully'})


def to_dict(row):
    pass 

def to_list(data):
    pass


if __name__ == "__main__":
    app.run(debug=True)
