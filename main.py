import logging

import uvicorn
from fastapi import FastAPI
import sqlite3
from typing import Optional

from utils import generateAccessToken
from pydantic import BaseModel

app = FastAPI()
database_name = "main"
class UserJoin(BaseModel):
    accessToken: str
    selectedProfile: str
    serverId: str

@app.post("/join")
def join(user: UserJoin):
    pass
@app.get("/users")
def get_all_users(username: Optional[str] = None):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    if username is None:
        cursor.execute('SELECT * FROM players')
        users = cursor.fetchall()
        connection.close()
        return users
    else:
        cursor.execute(f'SELECT * FROM players WHERE username = \'{username}\'')
        users = cursor.fetchall()
        connection.close()
        return users
@app.get("/auth")
def auth(username: Optional[str] = None, password: Optional[str] = None):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    if username is None or password is None:
        return "Error: post username and password"
    else:
        cursor.execute(f'SELECT * FROM players WHERE username = \'{username}\'')
        user = cursor.fetchone()
        print(user[2])
        if user[2] == password:
            access_token = generateAccessToken()
            cursor.execute(f'UPDATE players SET access_token = \'{access_token}\' WHERE username = \'{username}\'')
            connection.commit()
            connection.close()
            return user
        else:
            connection.close()
            return "Неверный пароль"
@app.get("/")
def home_page():
    return {"message": "Hello снегопад :з"}

if __name__ == '__main__':
    uvicorn.run(app,
                host="127.0.0.1",
                port=443,
                log_level="debug",
                reload=False,
                workers=1)