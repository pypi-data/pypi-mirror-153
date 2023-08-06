import json
import requests
from sqlalchemy import create_engine
import pytest
import time
from agent_service.main import get_password_hash, pwd_context, JWT_SECRET, JWT_ALGORITHM, list_companies, list_reviews
import jwt

AUTH_URL = 'http://localhost:8011/auth'
COMPANY_URL = 'http://localhost:8011/api/companies'

db = create_engine('postgresql://postgres:postgres@localhost:5437/postgres')


def generate_auth(id=0, role='user'):
    return {'Authorization': jwt.encode({'id': id, 'username': 'username 1', 'role': role}, JWT_SECRET, algorithm=JWT_ALGORITHM)}


@pytest.fixture(scope="session", autouse=True)
def before_tests(request):
    time.sleep(30)


def reset_table(number_of_rows=0, role=None):
    with db.connect() as connection:
        connection.execute("delete from users")
        
        if role == None:
            for i in range(number_of_rows):
                connection.execute("""
                    insert into users (id, username, password, first_name, last_name, email, role) values (%s, %s, %s, %s, %s, %s, %s)
                """, (f'{i+1}', f'username {i+1}', get_password_hash(f'password {i+1}'), f'first_name {i+1}', f'last_name {i+1}', f'email {i+1}', f'role {i+1}'))
        else:
            for i in range(number_of_rows):
                connection.execute("""
                    insert into users (id, username, password, first_name, last_name, email, role) values (%s, %s, %s, %s, %s, %s, %s)
                """, (f'{i+1}', f'username {i+1}', get_password_hash(f'password {i+1}'), f'first_name {i+1}', f'last_name {i+1}', f'email {i+1}', role))


def reset_company_table(number_of_rows=0, active=True, owner_id=0):
    with db.connect() as connection:
        connection.execute("delete from company")
        for i in range(number_of_rows):
            connection.execute("""
                insert into company (id, name, description, job_positions, address, city, active, owner_id) values (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (f'{i+1}', f'name {i+1}', f'description {i+1}', f'job_positions {i+1}', f'address {i+1}', f'city {i+1}', active, owner_id))


def reset_review_table(number_of_rows=0):
    with db.connect() as connection:
        connection.execute("delete from review")
        for i in range(number_of_rows):
            connection.execute("""
                insert into review (id, text_comment, payment_review, interview_review, company_id, author_id) values (%s, %s, %s, %s, %s, %s)
            """, (f'{i+1}', f'text_comment {i+1}', f'payment_review {i+1}', f'interview_review {i+1}', 0, 0))


def check_companies(companies: list, limit=7, offset_check=lambda x: x+1, active=True):
    assert len(companies) == limit
    for i in range(limit):
        assert companies[i]['id'] == offset_check(i)

        assert companies[i]['name'] == f'name {offset_check(i)}'
        assert companies[i]['description'] == f'description {offset_check(i)}'
        assert companies[i]['job_positions'] == f'job_positions {offset_check(i)}'
        assert companies[i]['address'] == f'address {offset_check(i)}'
        assert companies[i]['city'] == f'city {offset_check(i)}'
        assert companies[i]['active'] == active
        assert companies[i]['owner_id'] == 0


def check_reviews(reviews: list, limit=7, offset_check=lambda x: x+1):
    assert len(reviews) == limit
    for i in range(limit):
        assert reviews[i]['id'] == offset_check(i)

        assert reviews[i]['text_comment'] == f'text_comment {offset_check(i)}'
        assert reviews[i]['payment_review'] == f'payment_review {offset_check(i)}'
        assert reviews[i]['interview_review'] == f'interview_review {offset_check(i)}'
        assert reviews[i]['company_id'] == 0
        assert reviews[i]['author_id'] == 0


def test_registration_missing_first_name():
    data = {
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'first_name'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_first_name():
    data = {
        'first_name': None,
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'first_name'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_first_name():
    data = {
        'first_name': '',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'first_name'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_missing_last_name():
    data = {
        'first_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'last_name'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_last_name():
    data = {
        'first_name': 'asd',
        'last_name': None,
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'last_name'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_last_name():
    data = {
        'first_name': 'asd',
        'last_name': '',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'last_name'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_missing_email():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'email'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_email():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': None,
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'email'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_email():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': '',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'email'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_missing_username():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_username():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': None,
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_username():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': '',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_missing_password():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_password():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': None,
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_password():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': '',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_missing_role():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'role'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_registration_null_role():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': None
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'role'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_registration_empty_role():
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': ''
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'role'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_registration_valid():
    reset_table()
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    with db.connect() as connection:
        users = list(connection.execute("select * from users"))
    assert len(users) == 1
    assert users[0]['username'] == 'asd'
    assert pwd_context.verify('asd', users[0]['password'])
    assert users[0]['first_name'] == 'asd'
    assert users[0]['last_name'] == 'asd'
    assert users[0]['email'] == 'asd'
    assert users[0]['role'] == 'asd'


def test_registration_taken_username():
    reset_table(1)
    data = {
        'first_name': 'asd',
        'last_name': 'asd',
        'email': 'asd',
        'username': 'username 1',
        'password': 'asd',
        'role': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 400
    body = json.loads(res.text)
    assert body['detail'] == 'Username already exists'


def test_login_missing_username():
    data = {
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_login_null_username():
    data = {
        'username': None,
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_login_empty_username():
    data = {
        'username': '',
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_login_missing_password():
    data = {
        'username': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_login_null_password():
    data = {
        'username': 'asd',
        'password': None
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_login_empty_password():
    data = {
        'username': 'asd',
        'password': ''
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_login_invalid_username():
    reset_table(1)
    data = {
        'username': 'asd',
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 400
    body = json.loads(res.text)
    assert body['detail'] == 'User not found'


def test_login_invalid_password():
    reset_table(1)
    data = {
        'username': 'username 1',
        'password': 'asd'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 400
    body = json.loads(res.text)
    assert body['detail'] == 'Bad password'


def test_login_valid():
    reset_table(1)
    data = {
        'username': 'username 1',
        'password': 'password 1'
    }
    res = requests.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['access_token'] == jwt.encode({
        'username': 'username 1',
        'id': list(db.execute("select * from users where username='username 1'"))[0]['id'],
        'role': 'role 1'
    }, JWT_SECRET, algorithm=JWT_ALGORITHM)


def test_auth_missing_token():
    res = requests.get(AUTH_URL)
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'
    
    
def test_auth_null_token():
    res = requests.get(AUTH_URL, headers={'Authorization': None})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


def test_auth_empty_token():
    res = requests.get(AUTH_URL, headers={'Authorization': ''})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


def test_auth_invalid_token():
    res = requests.get(AUTH_URL, headers={'Authorization': 'asd'})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


def test_auth_invalid_user():
    res = requests.get(AUTH_URL, headers={'Authorization': jwt.encode({'username': 'asd'}, JWT_SECRET, algorithm=JWT_ALGORITHM)})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'User not found'


def test_auth_invalid_user():
    reset_table(1)
    res = requests.get(AUTH_URL, headers={'Authorization': jwt.encode({'username': 'username 1'}, JWT_SECRET, algorithm=JWT_ALGORITHM)})
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['username'] == 'username 1'
    assert body['id'] == list(db.execute("select * from users where username='username 1'"))[0]['id']
    

def test_company_registration_missing_name():
    data = {
        'description': 'asd',
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_company_registration_null_name():
    data = {
        'name': None,
        'description': 'asd',
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_company_registration_empty_name():
    data = {
        'name': '',
        'description': 'asd',
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_company_registration_missing_description():
    data = {
        'name': 'asd',
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_company_registration_null_description():
    data = {
        'name': 'asd',
        'description': None,
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_company_registration_empty_description():
    data = {
        'name': 'asd',
        'description': '',
        'address': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_company_registration_missing_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_company_registration_null_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': None,
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_company_registration_empty_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': '',
        'city': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_company_registration_missing_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_company_registration_null_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'city': None
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_company_registration_empty_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'city': ''
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_company_registration_valid():
    reset_table(1, 'user')
    reset_company_table()
    data = {
        'name': 'name 1',
        'description': 'description 1',
        'address': 'address 1',
        'city': 'city 1'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data, headers=generate_auth(list(db.execute("select * from users where username='username 1'"))[0]['id']))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None


def test_company_registration_taken_name():
    reset_table(1, 'user')
    reset_company_table(1, False)
    data = {
        'name': 'name 1',
        'description': 'description 1',
        'address': 'address 1',
        'city': 'city 1'
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data, headers=generate_auth(list(db.execute("select * from users where username='username 1'"))[0]['id']))
    assert res.status_code == 400
    body = json.loads(res.text)
    assert body['detail'] == 'Name already exists'


def test_update_company_missing_name():
    data = {
        'description': 'asd',
        'job_positions': 'asd',
        'address': 'asd',
        'city': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_update_company_null_name():
    data = {
        'name': None,
        'description': 'asd',
        'job_positions': 'asd',
        'address': 'asd',
        'city': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_update_company_empty_name():
    data = {
        'name': '',
        'description': 'asd',
        'address': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'name'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_update_company_missing_description():
    data = {
        'name': 'asd',
        'address': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_update_company_null_description():
    data = {
        'name': 'asd',
        'description': None,
        'address': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_update_company_empty_description():
    data = {
        'name': 'asd',
        'description': '',
        'address': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'description'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_update_company_missing_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_update_company_null_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': None,
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_update_company_empty_address():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': '',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'address'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_update_company_missing_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_update_company_null_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'city': None,
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_update_company_empty_city():
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'city': '',
        'job_positions': 'asd',
        'active': True
    }
    res = requests.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_update_company_valid():
    reset_table(1, 'owner')
    reset_company_table(1)
    data = {
        'name': 'asd',
        'description': 'asd',
        'address': 'asd',
        'city': 'asd',
        'job_positions': 'asd',
        'active': True,
        'owner_id': 1
    }
    res = requests.put(f"{COMPANY_URL}/" + str(list(db.execute("select * from company where name='name 1'"))[0]['id']), json=data, headers=generate_auth(1, 'owner'))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None
    company = list(db.execute("select * from company where name='name 1'"))[0]
    assert company['name'] == 'name 1'
    assert company['description'] == 'asd'
    assert company['address'] == 'asd'
    assert company['city'] == 'asd'
    assert company['job_positions'] == 'asd'
    assert company['active'] == True


def test_read_companies():
    reset_table(1)
    reset_company_table(10)

    res = requests.get(COMPANY_URL, headers=generate_auth(1))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] == f'/companies?offset=7&limit=7'
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 7
    check_companies(body['results'])


def test_read_companies_with_offset():
    reset_table(1)
    reset_company_table(10)

    res = requests.get(f'{COMPANY_URL}?offset=7', headers=generate_auth(1))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == f'/companies?offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 3
    check_companies(body['results'], 3, lambda x: 8+x)


def test_read_companies_with_limit():
    reset_table(1)
    reset_company_table(10)

    res = requests.get(f'{COMPANY_URL}?limit=10', headers=generate_auth(1))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 10
    assert body['size'] == 10
    check_companies(body['results'], 10)


def test_read_company_requests():
    reset_table(1, 'admin')
    reset_company_table(10, False)

    res = requests.get(COMPANY_URL + "/requests", headers=generate_auth(1, 'admin'))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] == f'/companies/requests?offset=7&limit=7'
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 7
    check_companies(body['results'], active=False)


def test_read_company_requests_with_offset():
    reset_table(1, 'admin')
    reset_company_table(10, active=False)

    res = requests.get(f'{COMPANY_URL}/requests?offset=7', headers=generate_auth(1, 'admin'))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == f'/companies/requests?offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 3
    check_companies(body['results'], 3, lambda x: 8+x, active=False)


def test_read_company_requests_with_limit():
    reset_table(1, 'admin')
    reset_company_table(10, active=False)

    res = requests.get(f'{COMPANY_URL}/requests?limit=10', headers=generate_auth(1, 'admin'))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 10
    assert body['size'] == 10
    check_companies(body['results'], 10, active=False)


def test_create_review_missing_text_comment():
    data = {
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'text_comment'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_create_review_null_text_comment():
    data = {
        'text_comment': None,
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'text_comment'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_create_review_empty_text_comment():
    data = {
        'text_comment': '',
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'text_comment'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_create_review_missing_payment_review():
    data = {
        'text_comment': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'payment_review'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_create_review_null_payment_review():
    data = {
        'text_comment': 'asd',
        'payment_review': None,
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'payment_review'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_create_review_empty_payment_review():
    data = {
        'text_comment': 'asd',
        'payment_review': '',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'payment_review'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_create_review_missing_interview_review():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'interview_review'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_create_review_null_interview_review():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': None,
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'interview_review'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_create_review_empty_interview_review():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': '',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'interview_review'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


def test_create_review_missing_company_id():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': 'asd'
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'company_id'
    assert body['detail'][0]['msg'] == 'field required'
    assert body['detail'][0]['type'] == 'value_error.missing'


def test_create_review_null_company_id():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': None
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'company_id'
    assert body['detail'][0]['msg'] == 'none is not an allowed value'
    assert body['detail'][0]['type'] == 'type_error.none.not_allowed'


def test_create_review_invalid_company_id():
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': ''
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'company_id'
    assert body['detail'][0]['msg'] == 'value is not a valid integer'
    assert body['detail'][0]['type'] == 'type_error.integer'


def test_create_review_valid():
    reset_table(1, 'user')
    reset_review_table()
    data = {
        'text_comment': 'asd',
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = requests.post(f"{COMPANY_URL}/review", json=data, headers=generate_auth(list(db.execute("select * from users where username='username 1'"))[0]['id'], 'user'))
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body is None


def test_read_reviews():
    reset_review_table(10)

    res = requests.get(f'{COMPANY_URL}/0/review', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] == f'/companies/0/review?offset=7&limit=7'
    assert body['offset'] == 0
    assert body['limit'] == 7
    assert body['size'] == 7
    check_reviews(body['results'])


def test_read_reviews_with_offset():
    reset_review_table(10)

    res = requests.get(f'{COMPANY_URL}/0/review?offset=7', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] == f'/companies/0/review?offset=0&limit=7'
    assert body['links']['next'] is None
    assert body['offset'] == 7
    assert body['limit'] == 7
    assert body['size'] == 3
    check_reviews(body['results'], 3, lambda x: 8+x)


def test_read_reviews_with_limit():
    reset_review_table(10)

    res = requests.get(f'{COMPANY_URL}/0/review?limit=10', headers=generate_auth())
    assert res.status_code == 200
    body = json.loads(res.text)
    assert body['links']['prev'] is None
    assert body['links']['next'] is None
    assert body['offset'] == 0
    assert body['limit'] == 10
    assert body['size'] == 10
    check_reviews(body['results'], 10)

