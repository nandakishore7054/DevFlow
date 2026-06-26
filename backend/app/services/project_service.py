from sqlalchemy.orm import Session
from ..models import Project
from ..schemas import ProjectCreate

def get_user_projects(db: Session, user_id: int):
    """Retrieve all projects for a specific user."""
    return db.query(Project).filter(Project.user_id == user_id).all()

def create_project(db: Session, project: ProjectCreate, user_id: int):
    """Create a new project associated with a user."""
    db_project = Project(
        name=project.name,
        description=project.description,
        user_id=user_id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project
