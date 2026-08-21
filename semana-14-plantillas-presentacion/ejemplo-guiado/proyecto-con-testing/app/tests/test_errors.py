def test_422_validation_error_format(client, auth_headers):
    response = client.post("/courses/", json={}, headers=auth_headers)
    assert response.status_code == 422
    data = response.json()
    assert data["error"] is True
    assert data["codigo"] == 422
    assert data["mensaje"] == "Datos invalidos"
    assert "detalles" in data
    assert len(data["detalles"]) > 0


def test_404_not_found_format(client, auth_headers):
    response = client.get("/courses/9999")
    assert response.status_code == 404
    data = response.json()
    assert data["error"] is True
    assert data["codigo"] == 404
    assert "no encontrado" in data["mensaje"].lower()


def test_403_forbidden_format(client, auth_headers, created_course):
    course_id = created_course["id"]
    response = client.delete(f"/courses/{course_id}", headers=auth_headers)
    assert response.status_code == 403
    data = response.json()
    assert data["error"] is True
    assert "permisos" in data["mensaje"].lower()
