from fastapi import FastAPI

app = FastAPI()


Books = {
    'book1': {'title': 'title one', 'author': 'author one'},
    'book2': {'title': 'title two', 'author': 'author two'},
    'book3': {'title': 'title three', 'author': 'author three'},
    'book4': {'title': 'title four', 'author': 'author four'}
}


@app.get('/')
async def read_all_books():
    return Books


@app.get('/books/{book_title}')
async def read_book(book_id: int):
    return {'book_id': book_id}