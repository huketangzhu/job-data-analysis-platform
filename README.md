# 招聘信息采集与分析平台
## Job Data Analysis Platform

一个基于 Python 的个人练手项目，用于实现招聘岗位数据的采集、清洗、存储、分析和可视化展示。

## 项目简介
本项目面向 Python 初学者与实习求职场景，目标是构建一个完整的小型数据分析系统。项目通过采集公开岗位样本数据，提取岗位名称、公司名称、城市、薪资、学历要求、经验要求等核心字段，并对数据进行清洗、结构化处理、数据库存储以及网页展示。

## 项目目标
- 学习 Python 数据采集与解析流程
- 学习 pandas 数据清洗与处理
- 学习 MySQL 数据库存储
- 学习 Flask Web 页面开发
- 完成一个可展示在 GitHub 和简历中的完整项目

## 功能规划
### V1 版本
- [ ] 采集岗位基础数据
- [ ] 将原始数据保存为 JSON / CSV
- [ ] 对岗位数据进行清洗和去重
- [ ] 将清洗后的数据存入 MySQL
- [ ] 使用 Flask 展示岗位列表
- [ ] 实现基础数据分析与图表可视化

### 后续可扩展功能
- [ ] 添加搜索和筛选功能
- [ ] 添加分页功能
- [ ] 添加更多图表分析
- [ ] 支持定时更新数据
- [ ] 部署到云服务器

## 技术栈
- Python 3
- Flask
- requests
- BeautifulSoup4 / lxml
- pandas
- MySQL
- SQLAlchemy
- HTML
- CSS
- JavaScript

## 项目结构
```text
job-data-analysis-platform/
│
├── app.py
├── config.py
├── crawler.py
├── clean_data.py
├── save_to_db.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│   ├── __init__.py
│   └── job.py
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── jobs.html
│   └── analysis.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── docs/
    └── project_design.md
