import json
import requests
from sqlalchemy import create_engine
import pytest
import time
from agent_service.main import get_password_hash, pwd_context, JWT_SECRET, JWT_ALGORITHM
import jwt

AUTH_URL = 'http://localhost:8011/auth'

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
