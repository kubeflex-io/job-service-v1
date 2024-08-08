from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import select, Session
from ..dependencies import get_session
from ..models import Job, JobCreate, JobUpdate, JobPublic
import uuid

router = APIRouter(
    prefix="/api/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=JobPublic)
def create_job(*, session: Session = Depends(get_session), job: JobCreate):
    db_job = Job.model_validate(job)
    db_job.id = str(uuid.uuid4())
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

@router.get("/", response_model=list[JobPublic])
def get_jobs(*, session: Session = Depends(get_session), offset: int = 0, limit: int = Query(default=100, le=100)):
    jobs = session.exec(select(Job).offset(offset).limit(limit)).all()
    if not jobs:
        raise HTTPException(status_code=404, detail="Jobs not found")
    return jobs

@router.get("/{job_id}", response_model=JobPublic)
def get_job(*, session: Session = Depends(get_session), job_id: str):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job

@router.patch("/{job_id}", response_model=JobPublic)
def update_job(*, session: Session = Depends(get_session), job_id: str, job: JobUpdate):
    db_job = session.get(Job, job_id)
    if not db_job:
        raise HTTPException(status_code=404, detail="Job not found")
    job_data = job.model_dump(exclude_unset=True)
    db_job.sqlmodel_update(job_data)
    session.add(db_job)
    session.commit()
    session.refresh(db_job)
    return db_job

@router.delete("/{job_id}")
def delete_job(*, session: Session = Depends(get_session), job_id: str):
    job = session.get(Job, job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    session.delete(job)
    session.commit()
    return {"ok": True}
