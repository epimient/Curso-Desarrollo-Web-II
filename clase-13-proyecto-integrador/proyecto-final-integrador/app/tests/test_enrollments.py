def test_create_enrollment(client, token, created_course):
    response = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 201
    data = response.json()
    assert data["student_id"] == 1
    assert data["status"] == "enrolled"


def test_create_enrollment_without_token(client, created_course):
    response = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    })
    assert response.status_code == 401


def test_duplicate_enrollment_fails(client, token, created_course):
    data = {"student_id": 1, "course_id": created_course["id"]}
    client.post("/enrollments/", json=data, headers={"Authorization": f"Bearer {token}"})
    response = client.post("/enrollments/", json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 400


def test_list_enrollments(client, token, created_course):
    data = {"student_id": 1, "course_id": created_course["id"]}
    client.post("/enrollments/", json=data, headers={"Authorization": f"Bearer {token}"})
    response = client.get("/enrollments/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_enrollment_by_id(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.get(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["id"] == eid


def test_get_enrollment_not_found(client, token):
    response = client.get("/enrollments/9999", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 404


def test_update_enrollment_grade(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.patch(f"/enrollments/{eid}", json={"grade": 95.5}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["grade"] == 95.5


def test_update_enrollment_status(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.patch(f"/enrollments/{eid}", json={"status": "completed"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "completed"


def test_delete_enrollment_as_admin(client, admin_headers, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers=admin_headers)
    eid = create_resp.json()["id"]
    response = client.delete(f"/enrollments/{eid}", headers=admin_headers)
    assert response.status_code == 204


def test_delete_enrollment_as_student_fails(client, token, created_course):
    create_resp = client.post("/enrollments/", json={
        "student_id": 1,
        "course_id": created_course["id"],
    }, headers={"Authorization": f"Bearer {token}"})
    eid = create_resp.json()["id"]
    response = client.delete(f"/enrollments/{eid}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
