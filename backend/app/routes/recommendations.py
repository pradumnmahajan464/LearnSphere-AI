"""
Recommendations route.
"""
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import RecommendationResponse
from ..services import get_current_user
from ..ml import get_recommendations

router = APIRouter(prefix="/api", tags=["recommendations"])


@router.get("/recommendations", response_model=List[RecommendationResponse])
def recommendations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    recs = get_recommendations(current_user.id, db)
    return [RecommendationResponse(**r) for r in recs]
