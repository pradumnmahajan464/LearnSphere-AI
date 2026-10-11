"""
Dashboard route — aggregated view for the logged-in student.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Subject, Topic, TopicProgress, QuizAttempt, Quiz
from ..schemas import DashboardResponse, SubjectListItem, QuizAttemptResponse
from ..services import get_current_user
from ..ml import get_recommendations

router = APIRouter(prefix="/api", tags=["dashboard"])


def _build_subject_list(user_id: int, db: Session) -> List[SubjectListItem]:
    subjects = db.query(Subject).all()
    completed_ids = {
        tp.topic_id
        for tp in db.query(TopicProgress)
        .filter(TopicProgress.user_id == user_id, TopicProgress.completed == True)
        .all()
    }
    result = []
    for s in subjects:
        topic_count = len(s.topics)
        completed_count = sum(1 for t in s.topics if t.id in completed_ids)
        pct = round(completed_count / topic_count * 100, 1) if topic_count else 0.0
        result.append(
            SubjectListItem(
                id=s.id,
                name=s.name,
                description=s.description,
                icon=s.icon,
                topic_count=topic_count,
                completed_count=completed_count,
                progress_pct=pct,
            )
        )
    return result


def _build_attempts(user_id: int, db: Session, limit: int = 5) -> List[QuizAttemptResponse]:
    attempts = (
        db.query(QuizAttempt)
        .filter(QuizAttempt.user_id == user_id)
        .order_by(QuizAttempt.attempted_at.desc())
        .limit(limit)
        .all()
    )
    result = []
    for a in attempts:
        result.append(
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
        )
    return result


@router.get("/dashboard", response_model=DashboardResponse)
def dashboard(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    subject_progress = _build_subject_list(current_user.id, db)

    all_attempts = db.query(QuizAttempt).filter(QuizAttempt.user_id == current_user.id).all()
    if all_attempts:
        avg = sum(
            a.score / a.total_questions * 100 for a in all_attempts if a.total_questions
        ) / len(all_attempts)
        quiz_avg = round(avg, 1)
    else:
        quiz_avg = 0.0

    completed_lessons = sum(s.completed_count for s in subject_progress)
    total_lessons = sum(s.topic_count for s in subject_progress)
    recent = _build_attempts(current_user.id, db)

    recs = get_recommendations(current_user.id, db)
    rec_topic = recs[0]["topic_title"] if recs else None

    return DashboardResponse(
        student_name=current_user.name,
        enrolled_subjects=len(subject_progress),
        quiz_average_pct=quiz_avg,
        completed_lessons=completed_lessons,
        total_lessons=total_lessons,
        subject_progress=subject_progress,
        recent_attempts=recent,
        recommended_topic=rec_topic,
    )
