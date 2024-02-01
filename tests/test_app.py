from fastapi.testclient import TestClient

from fast_zero.app import app


def test_root_deve_retornar_200_e_ola_mundo():
    client = TestClient(app) # Arrange

    response = client.get('/') # Act

    assert response.status_code == 200 # Assert
    assert response.json() == {'message': 'ALO ALO MARCIANO'} # Assert
