from fastapi import FastAPI

from fast_zero.routes import auth, users
from fast_zero.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)


@app.get('/', response_model=Message, status_code=200)
def read_root():
    return {'message': 'ALO ALO MARCIANO'}
