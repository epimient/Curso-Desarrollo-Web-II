def test_x_process_time_header(client):
    response = client.get("/health/")
    assert response.status_code == 200
    assert "x-process-time" in response.headers
    assert response.headers["x-process-time"] is not None


def test_cors_headers_present(client):
    response = client.options(
        "/courses/",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers


def test_cors_specific_origin(client):
    origin = "http://localhost:5173"
    response = client.options(
        "/courses/",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.headers["access-control-allow-origin"] == origin


def test_cors_rejects_unauthorized_origin(client):
    response = client.options(
        "/courses/",
        headers={
            "Origin": "http://evil.com",
            "Access-Control-Request-Method": "GET",
        },
    )
    allow_origin = response.headers.get("access-control-allow-origin", "")
    assert "evil.com" not in allow_origin
