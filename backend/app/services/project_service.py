from sqlalchemy.orm import Session
from ..models import Project
from ..schemas import ProjectCreate, ProjectUpdate

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

def get_project_by_id(db: Session, project_id: int):
    """Retrieve a project by its ID."""
    return db.query(Project).filter(Project.id == project_id).first()

def update_project(db: Session, db_project: Project, project_update: ProjectUpdate):
    """Update a project's details."""
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, db_project: Project):
    """Delete a project from the database."""
    db.delete(db_project)
    db.commit()
