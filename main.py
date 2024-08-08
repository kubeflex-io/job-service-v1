from fastapi import FastAPI

from app.routers import jobs, jobcategories

app = FastAPI()

app.include_router(jobs.router)
app.include_router(jobcategories.router)

# @app.get("/")
# async def root():
#     return {"message": "Job Service!"}
