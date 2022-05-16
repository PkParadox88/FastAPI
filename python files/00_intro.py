'''
Install fastapi
Install uvicorn
'''

from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def first_api():
    return {'name': 'sherlock', 'job': 'Mentalist'}
