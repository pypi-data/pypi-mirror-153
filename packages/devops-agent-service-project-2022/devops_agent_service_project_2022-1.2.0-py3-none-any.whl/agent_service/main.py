from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from passlib.context import CryptContext
import uvicorn
import jwt
import json
from pathlib import Path
from fastapi.templating import Jinja2Templates
import requests
import os


BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))

app = FastAPI(title='Agent Service API')
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@agent_service_db:5432/postgres')

if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

db = create_engine(DATABASE_URL)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8011'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

AUTH_URL = '/auth'

JWT_SECRET = 'auth_service_secret'
JWT_ALGORITHM = 'HS256'


class Registration(BaseModel):
    first_name: str = Field(description='First Name', min_length=1)
    last_name: str = Field(description='Last Name', min_length=1)
    email: str = Field(description='Email', min_length=1)
    username: str = Field(description='Username', min_length=1)
    password: str = Field(description='Password', min_length=1)
    role: str = Field(description='Role', min_length=1)
    

class Login(BaseModel):
    username: str = Field(description='Username', min_length=1)
    password: str = Field(description='Password', min_length=1)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_current_user(request: Request):
    try:
        return get_user(jwt.decode(request.headers['Authorization'], JWT_SECRET, algorithms=[JWT_ALGORITHM])['id'])
    except:
        return None

def get_user(id: int):
    with db.connect() as connection:
        return dict(list(connection.execute('select * from users where id=%s', (id,)))[0])


def generate_offer_auth():
    return {'Authorization': 'agent_application_api_key'}


def auth_req(request: Request):
    try:
        data = jwt.decode(request.headers['Authorization'], JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except:
        raise HTTPException(status_code=401, detail='Invalid token')
    with db.connect() as connection:
        users = list(connection.execute("select * from users where username=%s", (data['username'],)))
        if not users:
            raise HTTPException(status_code=401, detail='User not found')
        user = users[0]
        return {
            'username': user['username'],
            'id': user['id'],
            'role': user['role']
        }


def authorization_check(request: Request, role='user'):
    user = auth_req(request)
    if role == 'any':
        return
    if user['role'] != role:
        raise HTTPException(status_code=403, detail='Forbidden')


@app.post(f"{AUTH_URL}/registration")
def registration(registration: Registration):
    with db.connect() as connection:
        try:
            connection.execute("""
            insert into users (username, password, first_name, last_name, email, role) values (%s, %s, %s, %s, %s, %s)
            """, (registration.username, get_password_hash(registration.password), registration.first_name, registration.last_name, registration.email, registration.role))
        except:
            raise HTTPException(status_code=400, detail="Username already exists")


@app.post(f"{AUTH_URL}/login")
def login(login: Login):
    with db.connect() as connection:
        users = list(connection.execute("select * from users where username=%s", (login.username,)))
        if not users:
            raise HTTPException(status_code=400, detail="User not found")
        user = users[0]            
        if not pwd_context.verify(login.password, user['password']):
            raise HTTPException(status_code=400, detail="Bad password")
        token = jwt.encode({
            'username': user['username'],
            'id': user['id'],
            'role': user['role']
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {"access_token": token}


@app.get(AUTH_URL)
def auth(request: Request):
    return auth_req(request)


@app.get(f"/view{AUTH_URL}/registration")
def view_registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/")
def view_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


def create_tables():
    with db.connect() as connection:
        with open("initdb.sql") as file:
            query = text(file.read())
            connection.execute(query)


def run_service():
    port = os.environ.get("PORT")
    if port != None:
        create_tables()
        uvicorn.run(app, host="0.0.0.0", port=port)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8011)


if __name__ == '__main__':
    run_service()
