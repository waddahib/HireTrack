from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy.orm import Session

from auth import create_access_token, hash_password, verify_password
from database import get_db
from models import Application, User


app = FastAPI()


# -------------------------
# Pydantic Models
# -------------------------

class JobApplicationCreate(BaseModel):
    company: str
    position: str
    status: str
    location: str | None = None
    job_url: str | None = None
    notes: str | None = None


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


# -------------------------
# Home
# -------------------------

@app.get("/")
def home():
    return {"message": "HireTrack API is running"}


# -------------------------
# User Registration
# -------------------------

@app.post("/register", response_model=UserResponse, status_code=201)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    email = user.email.lower()

    existing_user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


# -------------------------
# User Login
# -------------------------

@app.post("/login", response_model=TokenResponse)
def login_user(
    login: LoginRequest,
    db: Session = Depends(get_db)
):
    email = login.email.lower()

    user = (
        db.query(User)
        .filter(User.email == email)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    password_is_correct = verify_password(
        login.password,
        user.hashed_password
    )

    if not password_is_correct:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# -------------------------
# Create Application
# -------------------------

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


# -------------------------
# Get All Applications
# -------------------------

@app.get("/applications")
def get_applications(
    db: Session = Depends(get_db)
):
    return (
        db.query(Application)
        .order_by(Application.id)
        .all()
    )


# -------------------------
# Get One Application
# -------------------------

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


# -------------------------
# Update Application
# -------------------------

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


# -------------------------
# Delete Application
# -------------------------

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