from fast_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')   # Act

    assert response.status_code == 200   # Assert
    assert response.json() == {'message': 'ALO ALO MARCIANO'}   # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@email.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@email.com',
        'id': 1,
    }


def test_create_user_already_registered(client, user):
    # Cria o usuário
    client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'existingalice@email.com',
            'password': 'existingsecret',
        },
    )

    # Mano o mesmo username do usuário criado na requisição
    response = client.post(
        '/users/',
        json={
            'username': 'alice',
            'email': 'alice@email.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 400
    assert response.json() == {'detail': 'Username already registered'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': user.username,
            'email': user.email,
            'password': user.password,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_update_user_not_found(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'newpassword',
        },
    )
    assert response.status_code == 401

    assert response.json() == {'detail': 'Not authenticated'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client, user):
    response = client.delete('users/2')

    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_get_user(client, user):
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json() == {
        'username': user.username,
        'email': user.email,
        'id': user.id,
    }


def test_get_user_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
