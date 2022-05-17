from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=50)
    description: Optional[str] = Field(title='Description of the book',
                                       min_length=1,
                                       max_length=100)
    rating: int = Field(gt=-1, lt=11)


Books = []


@app.get('/')
async def read_all_books():
    return Books


@app.post('/')
async def add_book(book: Book):
    Books.append(book)
    return book
