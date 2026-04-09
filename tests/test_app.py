import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as app_activities

INITIAL_ACTIVITIES = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"],
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"],
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"],
    },
    "Basketball": {
        "description": "Team basketball games and practice",
        "schedule": "Tuesdays and Thursdays, 4:30 PM - 6:00 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"],
    },
    "Soccer": {
        "description": "Competitive soccer matches and training",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["james@mergington.edu", "sarah@mergington.edu"],
    },
    "Art Club": {
        "description": "Painting, drawing, and sculpture workshop",
        "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["isabella@mergington.edu"],
    },
    "Music Ensemble": {
        "description": "Orchestra and band performance group",
        "schedule": "Mondays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 25,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"],
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["noah@mergington.edu"],
    },
    "Science Club": {
        "description": "Hands-on experiments and scientific exploration",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["ava@mergington.edu", "ethan@mergington.edu"],
    },
}

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    app_activities.clear()
    app_activities.update(copy.deepcopy(INITIAL_ACTIVITIES))
    yield
    app_activities.clear()
    app_activities.update(copy.deepcopy(INITIAL_ACTIVITIES))


def test_get_activities_returns_activity_list():
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["schedule"] == "Fridays, 3:30 PM - 5:00 PM"
    assert activities["Chess Club"]["participants"] == ["michael@mergington.edu", "daniel@mergington.edu"]


def test_signup_for_activity_adds_participant():
    participant_email = "newstudent@mergington.edu"
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {participant_email} for Chess Club"}
    assert participant_email in app_activities["Chess Club"]["participants"]


def test_signup_for_activity_duplicate_returns_400():
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael%40mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_from_activity_removes_participant():
    response = client.delete(
        "/activities/Chess%20Club/signup?email=michael%40mergington.edu"
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Unregistered michael@mergington.edu from Chess Club"}
    assert "michael@mergington.edu" not in app_activities["Chess Club"]["participants"]


def test_unregister_not_signed_up_returns_400():
    response = client.delete(
        "/activities/Chess%20Club/signup?email=notregistered%40mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"
