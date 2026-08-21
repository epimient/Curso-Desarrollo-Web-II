def test_list_courses_empty(client):
    response = client.get("/courses/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_course_without_token(client, course_data):
    response = client.post("/courses/", json=course_data)
    assert response.status_code == 401


def test_create_course_with_token(client, auth_headers, course_data):
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == course_data["name"]
    assert data["credits"] == course_data["credits"]
    assert data["active"] is True


def test_create_duplicate_course(client, auth_headers, course_data):
    client.post("/courses/", json=course_data, headers=auth_headers)
    response = client.post("/courses/", json=course_data, headers=auth_headers)
    assert response.status_code == 400
    assert response.json()["mensaje"] == "El curso ya existe"


def test_get_course_by_id(client, auth_headers, course_data, created_course):
    course_id = created_course["id"]
    response = client.get(f"/courses/{course_id}")
    assert response.status_code == 200
    assert response.json()["name"] == course_data["name"]


def test_get_course_not_found(client):
    response = client.get("/courses/9999")
    assert response.status_code == 404


def test_delete_course_as_student(client, auth_headers, created_course):
    course_id = created_course["id"]
    response = client.delete(f"/courses/{course_id}", headers=auth_headers)
    assert response.status_code == 403


def test_delete_course_as_admin(client, admin_headers, created_course):
    course_id = created_course["id"]
    response = client.delete(f"/courses/{course_id}", headers=admin_headers)
    assert response.status_code == 200
    assert response.json()["detail"] == "Course deleted"


def test_delete_course_not_found(client, admin_headers):
    response = client.delete("/courses/9999", headers=admin_headers)
    assert response.status_code == 404
