from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ...database import get_db
from ...schemas import ProjectCreate, ProjectResponse, ProjectUpdate
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

def get_project_or_404_403(db: Session, project_id: int, current_user: User):
    """Helper function to fetch a project and verify ownership/existence."""
    project = project_service.get_project_by_id(db, project_id=project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if project.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this project")
    return project

@router.get("/{project_id}", response_model=ProjectResponse)
def read_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retrieve a specific project by ID.
    Ensures the user owns the project.
    """
    return get_project_or_404_403(db, project_id, current_user)

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a specific project by ID.
    Ensures the user owns the project before updating.
    """
    project = get_project_or_404_403(db, project_id, current_user)
    return project_service.update_project(db, db_project=project, project_update=project_update)

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a specific project by ID.
    Ensures the user owns the project before deleting.
    """
    project = get_project_or_404_403(db, project_id, current_user)
    project_service.delete_project(db, db_project=project)
