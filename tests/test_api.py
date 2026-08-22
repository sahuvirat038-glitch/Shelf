# Test a GET endpoint
def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


# Test a POST endpoint with payload
def test_create_item(client):
    payload = {"name": "Test Item", "price": 10.5}
    response = client.post("/items/", json=payload)

    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"
    assert "id" in response.json()


# Test error handling / validation
def test_create_item_invalid_data(client):
    payload = {"price": "not-a-number"}  # Missing 'name', invalid 'price'
    response = client.post("/items/", json=payload)

    assert response.status_code == 422  # FastAPI automated validation error
