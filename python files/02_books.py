from fastapi import FastAPI
from enum import Enum

app = FastAPI()


Books = {
    'book1': {'title': 'title one', 'author': 'author one'},
    'book2': {'title': 'title two', 'author': 'author two'},
    'book3': {'title': 'title three', 'author': 'author three'},
    'book4': {'title': 'title four', 'author': 'author four'}
}


class DirectionName(str, Enum):
    north = 'North'
    south = 'South'


@app.get('/')
async def read_all_books():
    return Books


@app.get('/direction/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {'direction': direction_name, 'look': 'UP'}
    if direction_name == DirectionName.south:
        return {'direction': direction_name, 'look': 'Down'}
