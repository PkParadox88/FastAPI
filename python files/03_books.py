from typing import Optional
from fastapi import FastAPI

app = FastAPI()


Books = {
    'book1': {'title': 'title one', 'author': 'author one'},
    'book2': {'title': 'title two', 'author': 'author two'},
    'book3': {'title': 'title three', 'author': 'author three'},
    'book4': {'title': 'title four', 'author': 'author four'}
}


@app.get('/')
async def skip(skip_book: Optional[str] = None):
    if skip_book:
        books2 = Books.copy()
        del books2[skip_book]
        return books2
    return Books


@app.get('/{book_name}')
async def read_book(book_name: str):
    return Books[book_name]


@app.post('/')
async def write_book(book_title, book_author):
    # get book no
    if len(Books) > 0:
        book_no = int(1)
        for book in Books:
            book_no += 1

        Books[f'book{book_no}'] = {'title': book_title, 'author': book_author}
    return Books


@app.put('/{book_name}')
async def update_book(book_name: str, book_title: str, book_author: str):
    book_info = {'title': book_title, 'author': book_author}
    Books[book_name] = book_info
    return book_info


@app.delete('/{book_name}')
async def delete_book(book_name):
    del Books[book_name]
    return f'This {book_name} has been deleted.'
