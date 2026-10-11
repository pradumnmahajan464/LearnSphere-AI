"""
Subjects and Topics routes.
"""
from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, Subject, Topic, TopicProgress
from ..schemas import SubjectListItem, SubjectResponse, TopicResponse
from ..services import get_current_user

router = APIRouter(prefix="/api", tags=["subjects"])


def _completed_ids(user_id: int, db: Session):
    return {
        tp.topic_id
        for tp in db.query(TopicProgress)
        .filter(TopicProgress.user_id == user_id, TopicProgress.completed == True)
        .all()
    }


@router.get("/subjects", response_model=List[SubjectListItem])
def list_subjects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    subjects = db.query(Subject).all()
    done = _completed_ids(current_user.id, db)
    result = []
    for s in subjects:
        tc = len(s.topics)
        cc = sum(1 for t in s.topics if t.id in done)
        result.append(
            SubjectListItem(
                id=s.id,
                name=s.name,
                description=s.description,
                icon=s.icon,
                topic_count=tc,
                completed_count=cc,
                progress_pct=round(cc / tc * 100, 1) if tc else 0.0,
            )
        )
    return result


@router.get("/subjects/{subject_id}", response_model=SubjectResponse)
def get_subject(
    subject_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    subject = db.get(Subject, subject_id)
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")

    done = _completed_ids(current_user.id, db)
    topics = [
        TopicResponse(
            id=t.id,
            subject_id=t.subject_id,
            title=t.title,
            notes=t.notes,
            difficulty=t.difficulty,
            order_index=t.order_index,
            completed=t.id in done,
        )
        for t in subject.topics
    ]
    tc = len(topics)
    cc = sum(1 for t in topics if t.completed)
    return SubjectResponse(
        id=subject.id,
        name=subject.name,
        description=subject.description,
        icon=subject.icon,
        topics=topics,
        progress_pct=round(cc / tc * 100, 1) if tc else 0.0,
    )


@router.post("/topics/{topic_id}/complete", status_code=status.HTTP_200_OK)
def complete_topic(
    topic_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    topic = db.get(Topic, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    progress = (
        db.query(TopicProgress)
        .filter(
            TopicProgress.user_id == current_user.id,
            TopicProgress.topic_id == topic_id,
        )
        .first()
    )
    if progress:
        progress.completed = True
        progress.completed_at = datetime.utcnow()
    else:
        progress = TopicProgress(
            user_id=current_user.id,
            topic_id=topic_id,
            completed=True,
            completed_at=datetime.utcnow(),
        )
        db.add(progress)
    db.commit()
    return {"message": "Topic marked as completed.", "topic_id": topic_id}
