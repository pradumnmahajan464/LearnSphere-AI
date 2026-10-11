"""
Backend tests for auth, quiz scoring, and recommendations.
Run from backend/: pytest tests/
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker

# ── In-memory test engine using StaticPool so all connections share one DB ────
TEST_DB_URL = "sqlite:///:memory:"
test_engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Override the database module BEFORE importing the app
from app.database import Base, get_db

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Now import the app (main.py runs create_all on the real engine,
# but we immediately override the dependency below)
from app.main import app

app.dependency_overrides[get_db] = override_get_db

from app.models.models import Subject, Topic, Quiz, Question


@pytest.fixture(autouse=True)
def setup_db():
    # Create all tables on the IN-MEMORY test engine
    Base.metadata.create_all(bind=test_engine)
    # Seed minimal test data
    db = TestSessionLocal()
    subject = Subject(name="Test Subject", description="For testing", icon="🧪")
    db.add(subject)
    db.flush()
    topic = Topic(
        subject_id=subject.id,
        title="Topic 1",
        notes="Notes",
        difficulty="Beginner",
        order_index=0,
    )
    db.add(topic)
    db.flush()
    quiz = Quiz(subject_id=subject.id, title="Test Quiz")
    db.add(quiz)
    db.flush()
    q1 = Question(
        quiz_id=quiz.id,
        question_text="Q1?",
        options=["A", "B", "C", "D"],
        correct_answer=0,
        explanation="A is correct",
    )
    q2 = Question(
        quiz_id=quiz.id,
        question_text="Q2?",
        options=["A", "B", "C", "D"],
        correct_answer=2,
        explanation="C is correct",
    )
    db.add_all([q1, q2])
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=test_engine)


client = TestClient(app)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def _register_and_login(email="test@example.com", password="secret123"):
    client.post(
        "/api/auth/register",
        json={"name": "Test User", "email": email, "password": password},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    return resp.json()["access_token"]


# ─────────────────────────────────────────────────────────────────────────────
# AUTH TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_register_success():
    resp = client.post(
        "/api/auth/register",
        json={"name": "Alice", "email": "alice@example.com", "password": "password1"},
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["email"] == "alice@example.com"
    assert "password_hash" not in data


def test_register_duplicate_email():
    client.post(
        "/api/auth/register",
        json={"name": "Bob", "email": "bob@example.com", "password": "password1"},
    )
    resp = client.post(
        "/api/auth/register",
        json={"name": "Bob2", "email": "bob@example.com", "password": "password2"},
    )
    assert resp.status_code == 409


def test_register_short_password():
    resp = client.post(
        "/api/auth/register",
        json={"name": "Charlie", "email": "charlie@example.com", "password": "abc"},
    )
    assert resp.status_code == 422


def test_login_success():
    client.post(
        "/api/auth/register",
        json={"name": "Dave", "email": "dave@example.com", "password": "password1"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "dave@example.com", "password": "password1"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_wrong_password():
    client.post(
        "/api/auth/register",
        json={"name": "Eve", "email": "eve@example.com", "password": "correct"},
    )
    resp = client.post(
        "/api/auth/login",
        json={"email": "eve@example.com", "password": "wrong"},
    )
    assert resp.status_code == 401


def test_me_authenticated():
    token = _register_and_login("me_test@example.com")
    resp = client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    assert resp.json()["email"] == "me_test@example.com"


def test_me_unauthenticated():
    resp = client.get("/api/auth/me")
    assert resp.status_code == 401


# ─────────────────────────────────────────────────────────────────────────────
# QUIZ SCORING TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_quiz_perfect_score():
    token = _register_and_login("quiz_perfect@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    # correct answers are index 0 and 2 (seeded above)
    resp = client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": [0, 2]},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == 2
    assert data["total_questions"] == 2
    assert data["accuracy_pct"] == 100.0


def test_quiz_zero_score():
    token = _register_and_login("quiz_zero@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    resp = client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": [1, 1]},
        headers=headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["score"] == 0
    assert data["accuracy_pct"] == 0.0


def test_quiz_wrong_answer_count():
    token = _register_and_login("quiz_bad@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    resp = client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": [0]},
        headers=headers,
    )
    assert resp.status_code == 422


def test_correct_answers_not_exposed():
    """Questions endpoint must not include correct_answer field."""
    token = _register_and_login("quiz_exposed@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    resp = client.get(f"/api/quizzes/{quiz_id}", headers=headers)
    assert resp.status_code == 200
    for q in resp.json()["questions"]:
        assert "correct_answer" not in q


# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION TESTS
# ─────────────────────────────────────────────────────────────────────────────

def test_recommendations_no_attempts():
    """With no quiz attempts, recommendations should still return data."""
    token = _register_and_login("rec_empty@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/api/recommendations", headers=headers)
    assert resp.status_code == 200
    recs = resp.json()
    assert len(recs) > 0
    for r in recs:
        assert "topic_title" in r
        assert "reason" in r
        assert "action" in r


def test_recommendations_after_perfect_quiz():
    """After 100% score, recommendation should be present with correct accuracy."""
    token = _register_and_login("rec_perfect@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": [0, 2]},
        headers=headers,
    )
    resp = client.get("/api/recommendations", headers=headers)
    recs = resp.json()
    test_rec = next((r for r in recs if "Test Subject" in r["subject_name"]), None)
    assert test_rec is not None
    assert test_rec["accuracy_pct"] == 100.0


def test_recommendations_after_low_score():
    """After < 50% score, recommendation reason should mention revision or below threshold."""
    token = _register_and_login("rec_low@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    quizzes = client.get("/api/quizzes", headers=headers).json()
    quiz_id = quizzes[0]["id"]
    # Score 0/2 = 0%
    client.post(
        f"/api/quizzes/{quiz_id}/submit",
        json={"answers": [1, 1]},
        headers=headers,
    )
    resp = client.get("/api/recommendations", headers=headers)
    recs = resp.json()
    test_rec = next((r for r in recs if "Test Subject" in r["subject_name"]), None)
    assert test_rec is not None
    reason_lower = test_rec["reason"].lower()
    assert "revis" in reason_lower or "below" in reason_lower


# ─────────────────────────────────────────────────────────────────────────────
# HEALTH CHECK
# ─────────────────────────────────────────────────────────────────────────────

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
