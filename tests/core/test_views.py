from django.test import Client


def test_index(client: Client) -> None:
    response = client.get('/')
    assert response.status_code == 200
