import json
import os
import pandas as pd


def parse_salary(salary_text):
    salary_min = None
    salary_max = None

    if not salary_text:
        return salary_min, salary_max

    salary_text = salary_text.strip()

    if "K-" in salary_text and salary_text.endswith("K"):
        try:
            parts = salary_text.replace("K", "").split("-")
            salary_min = int(parts[0]) * 1000
            salary_max = int(parts[1]) * 1000
        except (ValueError, IndexError):
            pass

    elif "元/天" in salary_text:
        try:
            daily_salary = int(salary_text.replace("元/天", ""))
            salary_min = daily_salary
            salary_max = daily_salary
        except ValueError:
            pass

    return salary_min, salary_max


def clean_job_data():
    input_path = "data/raw/raw_jobs.json"
    output_dir = "data/processed"
    output_path = os.path.join(output_dir, "clean_jobs.csv")

    if not os.path.exists(input_path):
        print(f"Raw data file not found: {input_path}")
        return

    with open(input_path, "r", encoding="utf-8") as f:
        raw_jobs = json.load(f)

    df = pd.DataFrame(raw_jobs)

    # 先把 tags 从 list 转成字符串
    if "tags" in df.columns:
        df["tags"] = df["tags"].apply(
            lambda x: ", ".join(x) if isinstance(x, list) else (str(x) if pd.notna(x) else "")
        )

    # 再去重
    df = df.drop_duplicates()

    # 填充缺失值
    df["job_name"] = df["job_name"].fillna("未知岗位")
    df["company_name"] = df["company_name"].fillna("未知公司")
    df["city"] = df["city"].fillna("未知城市")
    df["salary"] = df["salary"].fillna("面议")
    df["education"] = df["education"].fillna("不限")
    df["experience"] = df["experience"].fillna("不限")
    df["publish_time"] = df["publish_time"].fillna("未知时间")
    df["job_url"] = df["job_url"].fillna("")

    # 解析薪资
    salary_parsed = df["salary"].apply(parse_salary)
    df["salary_min"] = salary_parsed.apply(lambda x: x[0])
    df["salary_max"] = salary_parsed.apply(lambda x: x[1])

    os.makedirs(output_dir, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")

    print(f"Successfully cleaned {len(df)} job records and saved to {output_path}")


if __name__ == "__main__":
    clean_job_data()