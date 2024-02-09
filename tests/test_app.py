def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')   # Act

    assert response.status_code == 200   # Assert
    assert response.json() == {'message': 'ALO ALO MARCIANO'}   # Assert
