def test_index(client):
    """Test the index route for service readiness."""
    response = client.get("/")
    
    assert response.status_code == 200
    
    assert response.json["status"] == "ready"


def test_invalid_endpoint(client, h_principal):
    """Test accessing an invalid endpoint."""
    response = client.get("/other", headers=h_principal)
    
    assert response.status_code == 404

    assert response.json["error"] == "NotFound"
