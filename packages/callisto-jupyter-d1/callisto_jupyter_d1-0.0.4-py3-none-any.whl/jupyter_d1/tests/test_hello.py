from fastapi.testclient import TestClient

from jupyter_d1 import app

client = TestClient(app)


def test_hello():
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_hello_there():
    response = client.get("/hello/there")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello there"}
