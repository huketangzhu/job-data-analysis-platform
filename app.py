from flask import Flask, render_template,request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pyecharts.charts import Bar, Pie
from pyecharts import options as opts

from config import Config
from models import Job

app = Flask(__name__)


def get_database_url():
    return (
        f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}"
        f"@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DATABASE}?charset=utf8mb4"
    )


engine = create_engine(get_database_url(), echo=False)
Session = sessionmaker(bind=engine)


@app.route("/")
def index():
    session = Session()

    jobs = session.query(Job).all()
    total_jobs = len(jobs)
    total_cities = len(set(job.city for job in jobs if job.city))

    salary_values = []
    for job in jobs:
        if job.salary_min is not None and job.salary_max is not None:
            avg_salary = (job.salary_min + job.salary_max) / 2
            salary_values.append(avg_salary)

    average_salary = round(sum(salary_values) / len(salary_values), 2) if salary_values else 0
    max_salary = max(salary_values) if salary_values else 0
    min_salary = min(salary_values) if salary_values else 0

    session.close()

    return render_template(
        "index.html",
        total_jobs=total_jobs,
        total_cities=total_cities,
        average_salary=average_salary,
        max_salary=max_salary,
        min_salary=min_salary
    )


@app.route("/jobs")
def jobs():
    session = Session()

    keyword = request.args.get("keyword", "").strip()
    city = request.args.get("city", "").strip()
    education = request.args.get("education", "").strip()

    query = session.query(Job)

    if keyword:
        query = query.filter(Job.job_name.contains(keyword))

    if city:
        query = query.filter(Job.city == city)

    if education:
        query = query.filter(Job.education == education)

    job_list = query.all()

    city_list = [item[0] for item in session.query(Job.city).distinct().all() if item[0]]
    education_list = [item[0] for item in session.query(Job.education).distinct().all() if item[0]]

    session.close()

    return render_template(
        "jobs.html",
        jobs=job_list,
        keyword=keyword,
        city=city,
        education=education,
        city_list=city_list,
        education_list=education_list
    )


@app.route("/analysis")
def analysis():
    session = Session()
    jobs = session.query(Job).all()
    session.close()

    city_stats = {}
    education_stats = {}
    salary_values = []

    for job in jobs:
        city = job.city or "未知城市"
        education = job.education or "不限"

        city_stats[city] = city_stats.get(city, 0) + 1
        education_stats[education] = education_stats.get(education, 0) + 1

        if job.salary_min is not None and job.salary_max is not None:
            avg_salary = (job.salary_min + job.salary_max) / 2
            salary_values.append(avg_salary)

    average_salary = round(sum(salary_values) / len(salary_values), 2) if salary_values else 0

    city_sorted = sorted(city_stats.items(), key=lambda x: x[1], reverse=True)
    education_sorted = sorted(education_stats.items(), key=lambda x: x[1], reverse=True)

    city_names = [item[0] for item in city_sorted]
    city_counts = [item[1] for item in city_sorted]

    education_data = [(item[0], item[1]) for item in education_sorted]

    city_bar = (
        Bar()
        .add_xaxis(city_names)
        .add_yaxis("岗位数量", city_counts)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="城市岗位数量统计"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)),
            yaxis_opts=opts.AxisOpts(name="数量")
        )
    )

    education_pie = (
        Pie()
        .add("", education_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="学历要求分布"))
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )

    city_bar_html = city_bar.render_embed()
    education_pie_html = education_pie.render_embed()

    return render_template(
        "analysis.html",
        average_salary=average_salary,
        city_bar_html=city_bar_html,
        education_pie_html=education_pie_html
    )


if __name__ == "__main__":
    app.run(debug=True)