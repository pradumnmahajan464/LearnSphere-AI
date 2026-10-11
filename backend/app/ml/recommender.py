"""
Rule-based recommendation engine for LearnSphere AI.

Thresholds (configurable via module-level constants):
  - accuracy < LOW_THRESHOLD  → revise the same topic
  - LOW_THRESHOLD ≤ accuracy < HIGH_THRESHOLD → extra practice on next topic
  - accuracy ≥ HIGH_THRESHOLD → advance to the next topic
"""
from __future__ import annotations
from typing import List, Optional
from sqlalchemy.orm import Session

from ..models import Subject, Topic, TopicProgress, Quiz, QuizAttempt

# ── Configurable thresholds ────────────────────────────────────────────────────
LOW_THRESHOLD = 50    # below this → revision
HIGH_THRESHOLD = 80   # at or above this → advance


def _accuracy(score: int, total: int) -> float:
    """Return accuracy as a percentage (0–100)."""
    if total == 0:
        return 0.0
    return round(score / total * 100, 1)


def _subject_accuracy(attempts: List[QuizAttempt], subject_quiz_ids: List[int]) -> Optional[float]:
    """Average accuracy across all attempts for quizzes in this subject."""
    relevant = [a for a in attempts if a.quiz_id in subject_quiz_ids]
    if not relevant:
        return None
    avg = sum(_accuracy(a.score, a.total_questions) for a in relevant) / len(relevant)
    return round(avg, 1)


def get_recommendations(user_id: int, db: Session) -> List[dict]:
    """
    Returns a list of recommendation dicts, one per subject, shaped as:
    {
        "subject_name": str,
        "topic_title": str,
        "reason": str,
        "action": str,
        "accuracy_pct": float | None,
    }
    """
    subjects: List[Subject] = db.query(Subject).all()
    all_attempts: List[QuizAttempt] = (
        db.query(QuizAttempt).filter(QuizAttempt.user_id == user_id).all()
    )
    completed_topic_ids = {
        tp.topic_id
        for tp in db.query(TopicProgress)
        .filter(TopicProgress.user_id == user_id, TopicProgress.completed == True)
        .all()
    }

    recommendations = []

    for subject in subjects:
        topics: List[Topic] = sorted(subject.topics, key=lambda t: t.order_index)
        if not topics:
            continue

        quiz_ids = [q.id for q in subject.quizzes]
        accuracy = _subject_accuracy(all_attempts, quiz_ids)

        # Find the first incomplete topic (or the last topic if all done)
        target_topic: Optional[Topic] = None
        for t in topics:
            if t.id not in completed_topic_ids:
                target_topic = t
                break
        if target_topic is None:
            target_topic = topics[-1]  # All complete — recommend last one as review

        if accuracy is None:
            # No attempts yet
            reason = "You haven't taken any quizzes for this subject yet."
            action = f"Start with the first topic: '{topics[0].title}' and then try the quiz."
            topic_title = topics[0].title
        elif accuracy < LOW_THRESHOLD:
            reason = (
                f"Your quiz accuracy is {accuracy}%, which is below {LOW_THRESHOLD}%. "
                "You should revise the material before moving on."
            )
            action = f"Re-read the notes for '{target_topic.title}' and retry the quiz."
            topic_title = target_topic.title
        elif accuracy < HIGH_THRESHOLD:
            reason = (
                f"Your quiz accuracy is {accuracy}%. Good progress! "
                "A little more practice will help solidify the concepts."
            )
            action = f"Practice extra exercises on '{target_topic.title}' and take the quiz again."
            topic_title = target_topic.title
        else:
            # Find next topic after target
            next_topic: Optional[Topic] = None
            found = False
            for t in topics:
                if found:
                    next_topic = t
                    break
                if t.id == target_topic.id:
                    found = True
            topic_title = next_topic.title if next_topic else target_topic.title
            reason = (
                f"Excellent work! Your accuracy is {accuracy}%, "
                f"which meets the advancement threshold of {HIGH_THRESHOLD}%."
            )
            action = (
                f"You're ready to advance to '{topic_title}'."
                if next_topic
                else f"You've completed all topics in {subject.name}. Consider reviewing '{topic_title}'."
            )

        recommendations.append({
            "subject_name": subject.name,
            "topic_title": topic_title,
            "reason": reason,
            "action": action,
            "accuracy_pct": accuracy,
        })

    return recommendations
