from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from models import Application


app = FastAPI()


class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str
    location: str | None = None
    job_url: str | None = None
    notes: str | None = None


@app.get("/")
def home():
    return {"message": "HireTrack API is running"}


@app.post("/applications")
def create_application(
    application: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    new_application = Application(
        **application.model_dump()
    )

    db.add(new_application)
    db.commit()
    db.refresh(new_application)

    return {
        "message": "Application added successfully",
        "application": new_application
    }


@app.get("/applications")
def get_applications(db: Session = Depends(get_db)):
    return db.query(Application).order_by(Application.id).all()


@app.get("/applications/{application_id}")
def get_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    return application


@app.put("/applications/{application_id}")
def update_application(
    application_id: int,
    updated_application: JobApplicationCreate,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    for field, value in updated_application.model_dump().items():
        setattr(application, field, value)

    db.commit()
    db.refresh(application)

    return {
        "message": "Application updated successfully",
        "application": application
    }


@app.delete("/applications/{application_id}")
def delete_application(
    application_id: int,
    db: Session = Depends(get_db)
):
    application = (
        db.query(Application)
        .filter(Application.id == application_id)
        .first()
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found"
        )

    db.delete(application)
    db.commit()

    return {
        "message": "Application deleted successfully",
        "application_id": application_id
    }