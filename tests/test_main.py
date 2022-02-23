from starlette.testclient import TestClient


def test_root_endpoint(testclient: TestClient):
    r = testclient.get("/")
    assert r.status_code == 200


def test_orga_identity(testclient: TestClient):
    data = {
        "bce": "BE0123.012.345",
        "name": "Trigu",
        "address": "Rue Ernest Bosh 6",
        "postal_code": "4123",
    }
    r = testclient.post("/orga_identity", json=data)
    assert r.status_code == 200, r.bce
    assert r.json()["bce"] == data["bce"]
