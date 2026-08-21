from sqlalchemy import Column, Integer, String, Text

from database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    company = Column(String(255), nullable=False)
    position = Column(String(255), nullable=False)
    status = Column(String(100), nullable=False)
    location = Column(String(255), nullable=True)
    job_url = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(320), unique=True, nullable=False, index=True)
    hashed_password = Column(Text, nullable=False)