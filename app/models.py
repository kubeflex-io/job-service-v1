from sqlmodel import Field, SQLModel, Relationship
import uuid

class JobCategoryBase(SQLModel):
    name: str = Field(index=True)

class JobCategory(JobCategoryBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    jobs: list["Job"] = Relationship(back_populates="category")

class JobCategoryCreate(JobCategoryBase):
    pass

class JobCategoryPublic(JobCategoryBase):
    id: int

class JobCategoryUpdate(SQLModel):
    name: str | None = None

class JobBase(SQLModel):
    title: str = Field(min_length=5, max_length=400)
    description: str
    owner_id: str
    category_id: int | None = Field(gt=0, foreign_key="jobcategory.id")

class Job(JobBase, table=True):
    id: str | None = Field(default=None, primary_key=True)
    category: JobCategory = Relationship(back_populates="jobs")

class JobPublic(JobBase):
    id: str

class JobCreate(JobBase):
    pass

class JobUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    category_id: int | None = None

class JobPublicWithCategory(JobPublic):
    jobcategory: JobCategoryPublic | None = None

class JobCategoryPublicWithJobs(JobCategoryPublic):
    jobs: list[JobPublic] = []

def create_db_and_tables():
    from .database import engine
    SQLModel.metadata.create_all(engine)
