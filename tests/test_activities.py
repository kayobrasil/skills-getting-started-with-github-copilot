import urllib.parse


def path(activity_name: str) -> str:
    return f"/activities/{urllib.parse.quote(activity_name)}/signup"


def test_get_activities(client):
    # Arrange

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@example.com"

    # Act
    resp = client.post(path(activity), params={"email": email})

    # Assert
    assert resp.status_code == 200
    assert resp.json()["message"] == f"Signed up {email} for {activity}"
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Programming Class"
    email = "dup@example.com"

    # Act - first signup
    r1 = client.post(path(activity), params={"email": email})
    assert r1.status_code == 200

    # Act - duplicate signup
    r2 = client.post(path(activity), params={"email": email})

    # Assert
    assert r2.status_code == 400
    assert r2.json()["detail"] == "Student already signed up"


def test_signup_activity_not_found(client):
    # Arrange
    activity = "No Such Activity"
    email = "x@example.com"

    # Act
    r = client.post(path(activity), params={"email": email})

    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == "Activity not found"


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    r = client.delete(path(activity), params={"email": email})

    # Assert
    assert r.status_code == 200
    assert r.json()["message"] == f"Unregistered {email} from {activity}"
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "noone@example.com"

    # Act
    r = client.delete(path(activity), params={"email": email})

    # Assert
    assert r.status_code == 404
    assert r.json()["detail"] == "Participant not found"
