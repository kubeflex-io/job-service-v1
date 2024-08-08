from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from ..dependencies import get_session
from ..models import JobCategory, JobCategoryCreate, JobCategoryUpdate, JobCategoryPublic

router = APIRouter(
    prefix="/api/jobcategories",
    tags=["jobcategories"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=JobCategoryPublic)
def create_jobcategory(*, session: Session = Depends(get_session), jobcategory: JobCategoryCreate):
    db_jobcategory = JobCategory.model_validate(jobcategory)
    session.add(db_jobcategory)
    session.commit()
    session.refresh(db_jobcategory)
    return db_jobcategory

@router.get("/", response_model=list[JobCategoryPublic])
def get_jobcategories(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    jobcategories = session.exec(select(JobCategory).offset(offset).limit(limit)).all()
    if not jobcategories:
        raise HTTPException(status_code=404, detail="Job Categories not found")
    return jobcategories

@router.get("/{jobcategory_id}", response_model=JobCategoryPublic)
def get_jobcategory(*, session: Session = Depends(get_session), jobcategory_id: int):
    jobcategory = session.get(JobCategory, jobcategory_id)
    if not jobcategory:
        raise HTTPException(status_code=404, detail="Job Category not found")
    return jobcategory

@router.patch("/{jobcategory_id}", response_model=JobCategoryPublic)
def update_job(*, session: Session = Depends(get_session), jobcategory_id: int, jobcategory: JobCategoryUpdate):
    db_jobcategory = session.get(JobCategory, jobcategory_id)
    if not db_jobcategory:
        raise HTTPException(status_code=404, detail="Job Category not found")
    jobcategory_data = jobcategory.model_dump(exclude_unset=True)
    db_jobcategory.sqlmodel_update(jobcategory_data)
    session.add(db_jobcategory)
    session.commit()
    session.refresh(db_jobcategory)
    return db_jobcategory

@router.delete("/{jobcategory_id}")
def delete_jobcategory(*, session: Session = Depends(get_session), jobcategory_id: int):
    jobcategory = session.get(JobCategory, jobcategory_id)
    if not jobcategory:
        raise HTTPException(status_code=404, detail="Job Category not found")
    session.delete(jobcategory)
    session.commit()
    return {"ok": True}
