from fastapi.testclient import TestClient
from agent_service.main import app, AUTH_URL, JWT_SECRET, JWT_ALGORITHM, get_password_hash
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
