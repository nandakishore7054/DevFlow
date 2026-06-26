from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from ...database import get_db
from ...schemas import ProjectCreate, ProjectResponse
from ...services import project_service
from ...models import User
from ..dependencies import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProjectResponse])
def read_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve all projects belonging to the currently authenticated user.
    """
    return project_service.get_user_projects(db=db, user_id=current_user.id)

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new project. 
    The project is automatically assigned to the authenticated user via their JWT token.
    """
    return project_service.create_project(db=db, project=project, user_id=current_user.id)
