"""
Pydantic schemas for request/response validation.
"""
from __future__ import annotations
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, field_validator


# ─── Auth ────────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def password_min_length(cls, v: str) -> str:
        if len(v) < 6:
            raise ValueError("Password must be at least 6 characters")
        return v

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Name must not be empty")
        return v.strip()


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Subjects / Topics ────────────────────────────────────────────────────────

class TopicResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    notes: str
    difficulty: str
    order_index: int
    completed: bool = False

    model_config = {"from_attributes": True}


class SubjectResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    topics: List[TopicResponse] = []
    progress_pct: float = 0.0

    model_config = {"from_attributes": True}


class SubjectListItem(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    topic_count: int
    completed_count: int
    progress_pct: float

    model_config = {"from_attributes": True}


# ─── Quizzes ──────────────────────────────────────────────────────────────────

class QuestionResponse(BaseModel):
    """Question shown during quiz — no correct_answer exposed."""
    id: int
    question_text: str
    options: List[str]

    model_config = {"from_attributes": True}


class QuizListItem(BaseModel):
    id: int
    subject_id: int
    subject_name: str
    title: str
    question_count: int

    model_config = {"from_attributes": True}


class QuizDetailResponse(BaseModel):
    id: int
    subject_id: int
    title: str
    questions: List[QuestionResponse]

    model_config = {"from_attributes": True}


class QuizSubmitRequest(BaseModel):
    answers: List[int]  # 0-based index for each question in order


class AnswerResult(BaseModel):
    question_id: int
    question_text: str
    selected: int
    correct: int
    is_correct: bool
    explanation: Optional[str] = None


class QuizSubmitResponse(BaseModel):
    attempt_id: int
    score: int
    total_questions: int
    accuracy_pct: float
    results: List[AnswerResult]


class QuizAttemptResponse(BaseModel):
    id: int
    quiz_id: int
    quiz_title: str
    subject_name: str
    score: int
    total_questions: int
    accuracy_pct: float
    attempted_at: datetime

    model_config = {"from_attributes": True}


# ─── Dashboard ────────────────────────────────────────────────────────────────

class DashboardResponse(BaseModel):
    student_name: str
    enrolled_subjects: int
    quiz_average_pct: float
    completed_lessons: int
    total_lessons: int
    subject_progress: List[SubjectListItem]
    recent_attempts: List[QuizAttemptResponse]
    recommended_topic: Optional[str] = None


# ─── Recommendations ─────────────────────────────────────────────────────────

class RecommendationResponse(BaseModel):
    subject_name: str
    topic_title: str
    reason: str
    action: str
    accuracy_pct: Optional[float] = None
