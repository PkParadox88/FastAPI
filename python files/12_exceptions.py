from typing import Optional
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_show):
        self.books_to_show = books_to_show


app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=100)
    rating: int = Field(gt=-1, lt=11)

    class Config:
        schema_extra = {
            'example': {
                'id': 'c4d1aa00-eda7-4a04-81a1-39c0404aaa60',
                'title': 'The Butterfly Effect',
                'author': 'Sherlock Holmes',
                'description': 'This is the best selling book on deduction and crime.',
                'rating': 9
            }
        }


class BookNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str
    description : Optional[str] = Field(
        None, title='description of the book',
        max_length=100,
        min_length=1
    )


Books = []


@app.exception_handler(NegativeNumberException)
async def negative_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418,
                        content={'message': f'Your input {exception.books_to_show} is negative'})


@app.get('/')
async def read_all_books(books_to_show: Optional[int] = 0):
    if books_to_show and books_to_show < 0:
        raise NegativeNumberException(books_to_show=books_to_show)

    if len(Books) < 1:
        books_no_api()
    if len(Books) >= books_to_show > 0:
        i = 1
        new_books = []
        while i <= books_to_show:
            new_books.append(Books[i-1])
            i += 1
            return new_books
    return Books


@app.post('/')
async def add_book(book: Book):
    Books.append(book)
    return book


@app.get('/book/{book_id}')
async def find_book(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x
    raise item_not_found()


@app.get('/book/rating/{book_id}', response_model=BookNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in Books:
        if x.id == book_id:
            return x
    raise item_not_found()


@app.put('/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for x in Books:
        counter += 1
        if x.id == book_id:
            Books[counter-1] = book
            return Books[counter-1]
    raise item_not_found()


@app.delete('/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for x in Books:
        counter += 1
        if x.id == book_id:
            del Books[counter-1]
            return f'{book_id} has been deleted.'
    raise item_not_found()


def books_no_api():
    book1 = Book(id='b4d1aa00-eda7-4a04-81a1-39c0404aaa60',
                 title='title one',
                 author='Author One',
                 description='Random One',
                 rating=4)
    book2 = Book(id='b4d1aa00-eda7-4a04-81a2-39c0404aaa60',
                 title='title one',
                 author='Author One',
                 description='Random One',
                 rating=5)
    book3 = Book(id='b4d1aa00-eda7-4a04-81a3-39c0404aaa60',
                 title='title one',
                 author='Author One',
                 description='Random One',
                 rating=6)

    Books.append(book1)
    Books.append(book2)
    Books.append(book3)


def item_not_found():
    raise HTTPException(status_code=404, detail='Book Not Found',
                        headers={'X-header-error': 'Nothing seen at UUID'})
