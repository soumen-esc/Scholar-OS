from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.database import get_db
from app.models.paper import Paper
from app.models.project import Project
from app.models.user import User
from app.schemas.paper import PaperCreate, PaperUpdate


router = APIRouter(
    prefix="/papers",
    tags=["Papers"]
)


@router.post("/")
def create_paper(
    paper: PaperCreate,
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    new_paper = Paper(
        project_id=project_id,
        title=paper.title,
        doi=paper.doi,
        file_name=paper.file_name,
        storage_key=paper.storage_key
    )

    db.add(new_paper)
    db.commit()
    db.refresh(new_paper)

    return {
        "message": "Paper created successfully",
        "paper_id": new_paper.id,
        "project_id": new_paper.project_id,
        "title": new_paper.title,
        "doi": new_paper.doi,
        "processing_status": new_paper.processing_status
    }


@router.get("/")
def get_papers(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.owner_id == current_user.id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    papers = db.query(Paper).filter(
        Paper.project_id == project_id
    ).all()

    return papers


@router.get("/{paper_id}")
def get_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    paper = db.query(Paper).join(
        Project,
        Paper.project_id == Project.id
    ).filter(
        Paper.id == paper_id,
        Project.owner_id == current_user.id
    ).first()

    if not paper:
        raise HTTPException(
            status_code=404,
            detail="Paper not found"
        )

    return paper


@router.put("/{paper_id}")
def update_paper(
    paper_id: int,
    paper_data: PaperUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    paper = db.query(Paper).join(
        Project,
        Paper.project_id == Project.id
    ).filter(
        Paper.id == paper_id,
        Project.owner_id == current_user.id
    ).first()

    if not paper:
        raise HTTPException(
            status_code=404,
            detail="Paper not found"
        )

    if paper_data.title is not None:
        paper.title = paper_data.title

    if paper_data.doi is not None:
        paper.doi = paper_data.doi

    if paper_data.processing_status is not None:
        paper.processing_status = paper_data.processing_status

    db.commit()
    db.refresh(paper)

    return {
        "message": "Paper updated successfully",
        "paper_id": paper.id,
        "project_id": paper.project_id,
        "title": paper.title,
        "doi": paper.doi,
        "processing_status": paper.processing_status
    }


@router.delete("/{paper_id}")
def delete_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    paper = db.query(Paper).join(
        Project,
        Paper.project_id == Project.id
    ).filter(
        Paper.id == paper_id,
        Project.owner_id == current_user.id
    ).first()

    if not paper:
        raise HTTPException(
            status_code=404,
            detail="Paper not found"
        )

    db.delete(paper)
    db.commit()

    return {
        "message": "Paper deleted successfully",
        "paper_id": paper_id
    }