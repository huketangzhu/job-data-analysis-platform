from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    job_name = Column(String(255), nullable=False)
    company_name = Column(String(255), nullable=False)
    city = Column(String(100), nullable=True)
    salary = Column(String(100), nullable=True)
    salary_min = Column(Integer, nullable=True)
    salary_max = Column(Integer, nullable=True)
    education = Column(String(100), nullable=True)
    experience = Column(String(100), nullable=True)
    tags = Column(Text, nullable=True)
    publish_time = Column(String(100), nullable=True)
    job_url = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)