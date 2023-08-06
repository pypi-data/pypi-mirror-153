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
COMPANY_URL = '/api/companies'
OFFER_URL = '/api/offers'

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


class Company(BaseModel):
    id: Optional[int] = Field(description='ID')
    name: str = Field(description='Name', min_length=1)
    description: str = Field(description='Description', min_length=1)
    job_positions: Optional[str] = Field(description='Job Positions')
    address: str = Field(description='Address', min_length=1)
    city: str = Field(description='City', min_length=1)
    owner_id: Optional[int] = Field(description='Owner ID')
    active: Optional[bool] = Field(description='Active')


class Review(BaseModel):
    id: Optional[int] = Field(description='ID')
    text_comment: str = Field(description='Comment', min_length=1)
    payment_review: str = Field(description='Payment Review', min_length=1)
    interview_review: str = Field(description='Interview Review', min_length=1)
    company_id: int = Field(description='Company ID')
    author_id: Optional[int] = Field(description='Author ID')


class Offer(BaseModel):
    position: str = Field(description='Offer Position', min_length=1)
    requirements: str = Field(description='Offer Requirements', min_length=1)
    description: str = Field(description='Offer Description', min_length=1)
    agent_application_link: str = Field(description='Offer Agent Application Link', min_length=1)


class NavigationLinks(BaseModel):
    base: str = Field('http://localhost:8011/api', description='API base URL')
    prev: Optional[str] = Field(None, description='Link to the previous page')
    next: Optional[str] = Field(None, description='Link to the next page')


class ResponseCompany(BaseModel):
    results: List[Company]
    links: NavigationLinks
    offset: int
    limit: int
    size: int


class ResponseReview(BaseModel):
    results: List[Review]
    links: NavigationLinks
    offset: int
    limit: int
    size: int


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


def list_companies(offset: int, limit: int, active: bool):    
    type = '' if active else '/requests'

    with db.connect() as connection:
        total_companies = len(list(connection.execute("""select * from company where active is %s""", (active))))
    prev_link = f'/companies{type}?offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
    next_link = f'/companies{type}?offset={offset + limit}&limit={limit}' if offset + limit < total_companies else None
    links = NavigationLinks(prev=prev_link, next=next_link)

    with db.connect() as connection:
        companies = list(connection.execute("""select * from company where active is %s order by id offset %s limit %s""", (active, offset, limit)))
    results = [Company.parse_obj(dict(company)) for company in companies]
    return ResponseCompany(results=results, links=links, offset=offset, limit=limit, size=len(results))


def list_reviews(offset: int, limit: int, company_id: int):
    with db.connect() as connection:
        total_reviews = len(list(connection.execute("""select * from review where company_id = %s""", (str(company_id)))))
    prev_link = f'/companies/{company_id}/review?offset={offset - limit}&limit={limit}' if offset - limit >= 0 else None
    next_link = f'/companies/{company_id}/review?offset={offset + limit}&limit={limit}' if offset + limit < total_reviews else None
    links = NavigationLinks(prev=prev_link, next=next_link)

    with db.connect() as connection:
        reviews = list(connection.execute("""select * from review where company_id = %s order by id offset %s limit %s""", (str(company_id), offset, limit)))
    results = [Review.parse_obj(dict(review)) for review in reviews]
    return ResponseReview(results=results, links=links, offset=offset, limit=limit, size=len(results))


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
    print(role == 'any')
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


@app.post(f"{COMPANY_URL}/registration")
def company_registration(request: Request, company: Company):
    authorization_check(request)
    
    with db.connect() as connection:
        try:
            connection.execute("""
            insert into company (name, description, job_positions, address, city, owner_id, active) values (%s, %s, %s, %s, %s, %s, %s)
            """, (company.name, company.description, company.job_positions, company.address, company.city, get_current_user(request)['id'], False))
            
            connection.execute(' '.join("""
                update users 
                set role=%s 
                where id=%s
            """.split()), ("owner-pending", get_current_user(request)['id']))
        except:
            raise HTTPException(status_code=400, detail="Name already exists")


@app.put(f"{COMPANY_URL}/" + "{company_id}")
def update_company(request: Request, company: Company, company_id: int = Query(-1)):
    set_owner_role = False;
    
    with db.connect() as connection:
        users = list(connection.execute("""select * from users where id = %s and role = %s""", (str(company.owner_id)), "owner-pending"))

        if len(users) > 0:
            authorization_check(request, 'admin')
            set_owner_role = True
        else:
            authorization_check(request, 'owner')

        connection.execute(' '.join(f"""
            update company 
            set description=%s, 
            job_positions=%s,
            address=%s, 
            city=%s, 
            active=%s 
            where id={company_id}
        """.split()), (company.description, company.job_positions,
                company.address, company.city, company.active))

        if set_owner_role:
            connection.execute(' '.join(f"""
                update users 
                set role=%s 
                where id={company.owner_id}
            """.split()), ("owner"))


@app.get(f"{COMPANY_URL}/requests")
def read_company_requests(request: Request, offset: int = Query(0), limit: int = Query(7)):
    authorization_check(request, 'admin')
    return list_companies(offset, limit, False)


@app.get(f"{COMPANY_URL}")
def read_companies(request: Request, offset: int = Query(0), limit: int = Query(7)):
    authorization_check(request, 'any')
    return list_companies(offset, limit, True)


@app.get(f"{COMPANY_URL}/owned")
def read_owned_company(request: Request):
    authorization_check(request, 'owner')
    owner_id = get_current_user(request)['id']

    with db.connect() as connection:
        companies = list(connection.execute("""select * from company where active is true and owner_id = %s limit %s""", (str(owner_id), '1')))
    results = [Company.parse_obj(dict(company)) for company in companies]
    return results[0] if len(results) > 0 else None


@app.post(f"{COMPANY_URL}/review")
def create_review(request: Request, review: Review):
    authorization_check(request)
    with db.connect() as connection:
        connection.execute("""
        insert into review (text_comment, payment_review, interview_review, company_id, author_id) values (%s, %s, %s, %s, %s)
        """, (review.text_comment, review.payment_review, review.interview_review, review.company_id, get_current_user(request)['id']))


@app.get(f"{COMPANY_URL}/" + "{company_id}/review")
def read_company_reviews(request: Request, offset: int = Query(0), limit: int = Query(7), company_id: int = Query(-1)):
    authorization_check(request, 'any')
    return list_reviews(offset, limit, company_id)


@app.post(f"{OFFER_URL}")
def create_offer(request: Request, offer: Offer):
    authorization_check(request, 'owner')
    requests.post('http://localhost:8000/api/offers', json=dict(offer), headers=generate_offer_auth())


@app.get(f"/view{AUTH_URL}/registration")
def view_registration(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@app.get("/")
def view_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.get(f"/view{COMPANY_URL}/registration")
def view_company_registration(request: Request):
    return templates.TemplateResponse("register_company.html", {"request": request})


@app.get(f"/view{COMPANY_URL}/requests")
def view_company_registration_requests(request: Request):
    return templates.TemplateResponse("company_requests.html", {"request": request})


@app.get(f"/view{COMPANY_URL}/owned")
def view_owned_company(request: Request):
    return templates.TemplateResponse("owned_company.html", {"request": request})


@app.get(f"/view{COMPANY_URL}")
def view_companies(request: Request):
    return templates.TemplateResponse("companies.html", {"request": request})


@app.get(f"/view{COMPANY_URL}/reviews/" + "{company_id}")
def view_reviews(request: Request, company_id: int = Query(-1)):
    return templates.TemplateResponse("reviews.html", {"request": request, "company_id": company_id})


@app.get(f"/view{COMPANY_URL}/offer")
def view_create_offer(request: Request):
    return templates.TemplateResponse("create_offer.html", {"request": request})


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
