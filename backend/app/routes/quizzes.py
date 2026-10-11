"""
Quiz routes: list, detail, submit, attempt history.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Quiz, Question, QuizAttempt
from ..schemas import (
    QuizListItem, QuizDetailResponse, QuestionResponse,
    QuizSubmitRequest, QuizSubmitResponse, AnswerResult,
    QuizAttemptResponse,
)
from ..services import get_current_user

router = APIRouter(prefix="/api", tags=["quizzes"])


@router.get("/quizzes", response_model=List[QuizListItem])
def list_quizzes(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quizzes = db.query(Quiz).all()
    return [
        QuizListItem(
            id=q.id,
            subject_id=q.subject_id,
            subject_name=q.subject.name,
            title=q.title,
            question_count=len(q.questions),
        )
        for q in quizzes
    ]


@router.get("/quizzes/{quiz_id}", response_model=QuizDetailResponse)
def get_quiz(
    quiz_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    # Expose only question text and options — NO correct_answer
    questions = [
        QuestionResponse(id=q.id, question_text=q.question_text, options=q.options)
        for q in quiz.questions
    ]
    return QuizDetailResponse(
        id=quiz.id,
        subject_id=quiz.subject_id,
        title=quiz.title,
        questions=questions,
    )


@router.post("/quizzes/{quiz_id}/submit", response_model=QuizSubmitResponse)
def submit_quiz(
    quiz_id: int,
    payload: QuizSubmitRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    quiz = db.get(Quiz, quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")

    questions: List[Question] = quiz.questions
    if len(payload.answers) != len(questions):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Expected {len(questions)} answers, received {len(payload.answers)}.",
        )

    score = 0
    results: List[AnswerResult] = []
    for q, selected in zip(questions, payload.answers):
        is_correct = selected == q.correct_answer
        if is_correct:
            score += 1
        results.append(
            AnswerResult(
                question_id=q.id,
                question_text=q.question_text,
                selected=selected,
                correct=q.correct_answer,
                is_correct=is_correct,
                explanation=q.explanation,
            )
        )

    attempt = QuizAttempt(
        user_id=current_user.id,
        quiz_id=quiz_id,
        score=score,
        total_questions=len(questions),
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return QuizSubmitResponse(
        attempt_id=attempt.id,
        score=score,
        total_questions=len(questions),
        accuracy_pct=round(score / len(questions) * 100, 1),
        results=results,
    )


@router.get("/quiz-attempts", response_model=List[QuizAttemptResponse])
def quiz_attempts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == current_user.id)
        .order_by(QuizAttempt.attempted_at.desc())
        .all()
    )
    return [
        QuizAttemptResponse(
            id=a.id,
            quiz_id=a.quiz_id,
            quiz_title=a.quiz.title,
            subject_name=a.quiz.subject.name,
            score=a.score,
            total_questions=a.total_questions,
            accuracy_pct=round(a.score / a.total_questions * 100, 1) if a.total_questions else 0.0,
            attempted_at=a.attempted_at,
        )
        for a in attempts
    ]
