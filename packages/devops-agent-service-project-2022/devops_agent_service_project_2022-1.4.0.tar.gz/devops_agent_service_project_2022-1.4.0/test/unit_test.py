from fastapi.testclient import TestClient
from agent_service.main import app, AUTH_URL, COMPANY_URL, JWT_SECRET, JWT_ALGORITHM, get_password_hash, list_companies, list_reviews
from mock import patch
import mock
import json
import jwt
from datetime import date


class TestDB:
    def connect(self):
        return self
    def execute(self, sql, params):
        return []
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, tb):
        pass


client = TestClient(app)
testDB = TestDB()


def generate_auth():
    return {'Authorization': jwt.encode({'id': 0}, JWT_SECRET, algorithm=JWT_ALGORITHM)}


def test_registration_missing_first_name():
    data = {
        'last_name': 'asd',
        'email': 'asd',
        'username': 'asd',
        'password': 'asd',
        'role': 'asd'
    }
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
        'password': 'asd'
    }
    res = client.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
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
    res = client.post(f'{AUTH_URL}/registration', json=data)
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
        'username': '',
        'password': 'asd',
        'role': ''
    }
    res = client.post(f'{AUTH_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'username'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


@patch('agent_service.main.db', testDB)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1}])
def test_registration_valid(param):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'first_name': 'asd',
            'last_name': 'asd',
            'email': 'asd',
            'username': 'asd',
            'password': 'asd',
            'role': 'asd'
        }
        res = client.post(f'{AUTH_URL}/registration', json=data)
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body is None
        db_spy.assert_called()


@patch('agent_service.main.db', testDB)
def test_registration_taken_username():
    with mock.patch("test.unit_test.testDB.execute") as db_mock:
        with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
            db_mock.side_effect = Exception()
            data = {
                'first_name': 'asd',
                'last_name': 'asd',
                'email': 'asd',
                'username': 'asd',
                'password': 'asd',
                'role': 'asd'
            }
            res = client.post(f'{AUTH_URL}/registration', json=data)
            assert res.status_code == 400
            body = json.loads(res.text)
            assert body['detail'] == 'Username already exists'
            db_spy.assert_called()


def test_login_missing_username():
    data = {
        'password': 'asd'
    }
    res = client.post(f'{AUTH_URL}/login', json=data)
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
    res = client.post(f'{AUTH_URL}/login', json=data)
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
    res = client.post(f'{AUTH_URL}/login', json=data)
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
    res = client.post(f'{AUTH_URL}/login', json=data)
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
    res = client.post(f'{AUTH_URL}/login', json=data)
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
    res = client.post(f'{AUTH_URL}/login', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'password'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


@patch('agent_service.main.db', testDB)
def test_login_invalid_username():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'username': 'asd',
            'password': 'asd'
        }
        res = client.post(f'{AUTH_URL}/login', json=data)
        assert res.status_code == 400
        body = json.loads(res.text)
        assert body['detail'] == 'User not found'
        db_spy.assert_called_once()
        db_spy.assert_called_with("select * from users where username=%s", ('asd',))


@patch('agent_service.main.db', testDB)
@patch('test.unit_test.testDB.execute', return_value=[{'password': get_password_hash('asd')}])
def test_login_invalid_password(param):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'username': 'asd',
            'password': 'qwe'
        }
        res = client.post(f'{AUTH_URL}/login', json=data)
        assert res.status_code == 400
        body = json.loads(res.text)
        assert body['detail'] == 'Bad password'
        db_spy.assert_called_once()
        db_spy.assert_called_with("select * from users where username=%s", ('asd',))


@patch('agent_service.main.db', testDB)
@patch('test.unit_test.testDB.execute', return_value=[{
    'username': 'asd', 
    'password': get_password_hash('asd'),
    'id': 1,
    'role': 'asd'
}])
def test_login_valid(param):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'username': 'asd',
            'password': 'asd'
        }
        res = client.post(f'{AUTH_URL}/login', json=data)
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body['access_token'] == jwt.encode({
            'username': 'asd',
            'id': 1,
            'role': 'asd'
        }, JWT_SECRET, algorithm=JWT_ALGORITHM)
        db_spy.assert_called_once()
        db_spy.assert_called_with("select * from users where username=%s", ('asd',))


def test_auth_missing_token():
    res = client.get(AUTH_URL)
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'
    
    
def test_auth_null_token():
    res = client.get(AUTH_URL, headers={'Authorization': None})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


def test_auth_empty_token():
    res = client.get(AUTH_URL, headers={'Authorization': ''})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


def test_auth_invalid_token():
    res = client.get(AUTH_URL, headers={'Authorization': 'asd'})
    assert res.status_code == 401
    body = json.loads(res.text)
    assert body['detail'] == 'Invalid token'


@patch('agent_service.main.db', testDB)
def test_auth_invalid_user():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        res = client.get(AUTH_URL, headers={'Authorization': jwt.encode({'username': 'asd'}, JWT_SECRET, algorithm=JWT_ALGORITHM)})
        assert res.status_code == 401
        body = json.loads(res.text)
        assert body['detail'] == 'User not found'
        db_spy.assert_called_once()
        db_spy.assert_called_with("select * from users where username=%s", ('asd',))


@patch('agent_service.main.db', testDB)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1, 'username': 'asd', 'role': 'asd'}])
def test_auth_valid(param):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        res = client.get(AUTH_URL, headers={'Authorization': jwt.encode({'username': 'asd'}, JWT_SECRET, algorithm=JWT_ALGORITHM)})
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body['username'] == 'asd'
        assert body['id'] == 1
        assert body['role'] == 'asd'
        db_spy.assert_called_once()
        db_spy.assert_called_with("select * from users where username=%s", ('asd',))


def test_company_registration_missing_name():
    data = {
        'description': 'asd',
        'address': 'asd',
        'city': 'asd'
    }
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


@patch('agent_service.main.db', testDB)
@patch('agent_service.main.auth_req', return_value={'role': 'user'})
@patch('agent_service.main.authorization_check', return_value=None)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1}])
def test_company_registration_valid(param1, param2, param3):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'name': 'asd',
            'description': 'asd',
            'address': 'asd',
            'city': 'asd'
        }
        res = client.post(f'{COMPANY_URL}/registration', json=data, headers=generate_auth())
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body is None
        db_spy.assert_called()


@patch('agent_service.main.db', testDB)
@patch('agent_service.main.auth_req', return_value={'role': 'user'})
@patch('agent_service.main.authorization_check', return_value=None)
def test_company_registration_taken_name(param, param2):
    with mock.patch("test.unit_test.testDB.execute") as db_mock:
        with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
            db_mock.side_effect = Exception()
            data = {
                'name': 'asd',
                'description': 'asd',
                'address': 'asd',
                'city': 'asd'
            }
            res = client.post(f'{COMPANY_URL}/registration', json=data, headers=generate_auth())
            assert res.status_code == 400
            body = json.loads(res.text)
            assert body['detail'] == 'Name already exists'
            db_spy.assert_called()


def test_update_company_missing_name():
    data = {
        'description': 'asd',
        'job_positions': 'asd',
        'address': 'asd',
        'city': 'asd',
        'active': True
    }
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
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
    res = client.post(f'{COMPANY_URL}/registration', json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'city'
    assert body['detail'][0]['msg'] == 'ensure this value has at least 1 characters'
    assert body['detail'][0]['type'] == 'value_error.any_str.min_length'
    assert body['detail'][0]['ctx']['limit_value'] == 1


@patch('agent_service.main.db', testDB)
@patch('agent_service.main.auth_req', return_value={'role': 'user'})
@patch('agent_service.main.authorization_check', return_value=None)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1}])
def test_update_company_valid(param, param2, param3):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'name': 'asd',
            'description': 'asd',
            'address': 'asd',
            'city': 'asd',
            'job_positions': 'asd',
            'active': True
        }
        res = client.put(f"{COMPANY_URL}/1", json=data)
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body is None
        db_spy.assert_called()


@patch("agent_service.main.db", testDB)
def test_list_companies_active():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:        
        res = list_companies(0, 10, True)
        assert res.offset == 0
        assert res.limit == 10
        assert res.size == 0
        assert res.links.prev == None
        assert res.links.next == None
        db_spy.assert_called()
        db_spy.assert_called_with(''
        ' '.join(f"""
            select * from company where active is %s order by id offset %s limit %s                        
        """.split()), (True, 0, 10))


@patch("agent_service.main.db", testDB)
def test_list_companies_inactive():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:        
        res = list_companies(0, 10, False)
        assert res.offset == 0
        assert res.limit == 10
        assert res.size == 0
        assert res.links.prev == None
        assert res.links.next == None
        db_spy.assert_called()
        db_spy.assert_called_with(''
        ' '.join(f"""
            select * from company where active is %s order by id offset %s limit %s                        
        """.split()), (False, 0, 10))


@patch('agent_service.main.db', testDB)
@patch('agent_service.main.auth_req', return_value={'role': 'owner'})
@patch('agent_service.main.authorization_check', return_value=None)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1, 'name': 'asd', 'description': 'asd', 'job_positions': 'asd', 'address': 'asd', 'city': 'asd', 'owner_id': 1, 'active': True}])
def test_read_owned_company(param, param2, param3):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        res = client.get(f"{COMPANY_URL}/owned", headers=generate_auth())
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body['id'] == 1
        assert body['name'] == 'asd'
        assert body['description'] == 'asd'
        assert body['job_positions'] == 'asd'
        assert body['address'] == 'asd'
        assert body['city'] == 'asd'
        assert body['owner_id'] == 1
        assert body['active'] == True
        db_spy.assert_called()


def test_create_review_missing_text_comment():
    data = {
        'payment_review': 'asd',
        'interview_review': 'asd',
        'company_id': 1
    }
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
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
    res = client.post(f"{COMPANY_URL}/review", json=data)
    assert res.status_code == 422
    body = json.loads(res.text)
    assert body['detail'][0]['loc'][0] == 'body'
    assert body['detail'][0]['loc'][1] == 'company_id'
    assert body['detail'][0]['msg'] == 'value is not a valid integer'
    assert body['detail'][0]['type'] == 'type_error.integer'


@patch('agent_service.main.db', testDB)
@patch('agent_service.main.auth_req', return_value={'role': 'user'})
@patch('agent_service.main.authorization_check', return_value=None)
@patch('test.unit_test.testDB.execute', return_value=[{'id': 1}])
def test_create_review_valid(param, param2, param3):
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:
        data = {
            'text_comment': 'asd',
            'payment_review': 'asd',
            'interview_review': 'asd',
            'company_id': 1
        }
        res = client.post(f"{COMPANY_URL}/review", json=data, headers=generate_auth())
        assert res.status_code == 200
        body = json.loads(res.text)
        assert body is None
        db_spy.assert_called()


@patch("agent_service.main.db", testDB)
def test_list_reviews():
    with patch.object(testDB, "execute", wraps=testDB.execute) as db_spy:        
        res = list_reviews(0, 10, 1)
        assert res.offset == 0
        assert res.limit == 10
        assert res.size == 0
        assert res.links.prev == None
        assert res.links.next == None
        db_spy.assert_called()
        db_spy.assert_called_with(''
        ' '.join(f"""select * from review where company_id = %s order by id offset %s limit %s""".split()), ("1", 0, 10))

