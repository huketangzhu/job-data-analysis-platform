import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from models import Base, Job


def get_database_url():
    return (
        f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}"
        f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}?charset=utf8mb4"
    )


def save_jobs_to_db():
    input_path = "data/processed/clean_jobs.csv"

    if not os.path.exists(input_path):
        print(f"Processed data file not found: {input_path}")
        return

    engine = create_engine(get_database_url(), echo=False)
    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(input_path)

    for _, row in df.iterrows():
        job = Job(
            job_name=row.get("job_name", "未知岗位"),
            company_name=row.get("company_name", "未知公司"),
            city=row.get("city", "未知城市"),
            salary=row.get("salary", "面议"),
            salary_min=None if pd.isna(row.get("salary_min")) else int(row.get("salary_min")),
            salary_max=None if pd.isna(row.get("salary_max")) else int(row.get("salary_max")),
            education=row.get("education", "不限"),
            experience=row.get("experience", "不限"),
            tags=row.get("tags", ""),
            publish_time=row.get("publish_time", "未知时间"),
            job_url=row.get("job_url", "")
        )
        session.add(job)

    session.commit()
    session.close()

    print(f"Successfully saved {len(df)} job records into MySQL database.")


if __name__ == "__main__":
    save_jobs_to_db()