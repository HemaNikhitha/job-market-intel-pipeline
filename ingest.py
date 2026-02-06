#!/usr/bin/env python3
"""
ingest.py
Generates an enterprise-style synthetic job dataset with broad role/title coverage.

Output: data/raw/jobs.csv
"""

from __future__ import annotations

import argparse
import os
import random
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from faker import Faker

fake = Faker()

US_CITIES = [
    ("Atlanta, GA", "GA"),
    ("Alpharetta, GA", "GA"),
    ("Austin, TX", "TX"),
    ("Seattle, WA", "WA"),
    ("San Francisco, CA", "CA"),
    ("San Jose, CA", "CA"),
    ("New York, NY", "NY"),
    ("Chicago, IL", "IL"),
    ("Boston, MA", "MA"),
    ("Denver, CO", "CO"),
    ("Dallas, TX", "TX"),
    ("Raleigh, NC", "NC"),
]

COMPANIES = [
    "Amazon", "Google", "Microsoft", "Apple", "Meta", "Netflix",
    "Uber", "Airbnb", "Salesforce", "Snowflake", "Databricks",
    "Stripe", "Block", "LinkedIn", "NVIDIA", "Oracle", "IBM",
    "Capital One", "Adobe", "Intuit", "Workday", "ServiceNow",
    "DoorDash", "Twilio", "Shopify", "Atlassian",
]

LEVELS = ["Entry", "Mid", "Senior", "Staff"]
LEVEL_PREFIX = {
    "Entry": ["Junior", "Entry-Level", "Associate"],
    "Mid": ["", ""],
    "Senior": ["Senior", "Lead"],
    "Staff": ["Staff", "Principal"],
}

# Broad functions (includes Developer variants)
FUNCTIONS = [
    "Software Engineer", "Software Developer", "Backend Engineer", "Backend Developer",
    "Full Stack Engineer", "Full Stack Developer", "Frontend Engineer", "Frontend Developer",
    "Mobile Engineer", "iOS Developer", "Android Developer",
    "Data Engineer", "Data Developer", "Analytics Engineer", "BI Developer",
    "Data Scientist", "Machine Learning Engineer", "ML Engineer", "MLOps Engineer", "AI Engineer",
    "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
    "Cloud Engineer", "Security Engineer", "QA Engineer", "Automation Engineer",
]

DOMAINS = [
    "Platform", "Infrastructure", "Distributed Systems", "APIs", "Payments", "Growth",
    "Data Platform", "Observability", "Security", "Cloud", "Search", "ML Platform",
    "Product Analytics", "ETL", "Streaming", "Warehouse", "Mobile", "Web",
]

TECH_MODIFIERS = [
    "Java", "Python", "Golang", "Node.js", "React", "Spark", "Kafka",
    "AWS", "GCP", "Azure", "Kubernetes", "Snowflake", "Databricks",
    "NLP", "Computer Vision", "LLM", "Terraform",
]

SKILL_CATALOG: Dict[str, List[str]] = {
    "core_swe": ["Git", "CI/CD", "Unit Testing", "System Design", "REST APIs", "OOP"],
    "java": ["Java", "Spring Boot", "Microservices", "JPA/Hibernate", "Maven/Gradle"],
    "python": ["Python", "FastAPI", "Flask"],
    "js_frontend": ["JavaScript", "TypeScript", "React", "HTML", "CSS"],
    "node": ["Node.js", "Express.js"],
    "go": ["Golang", "gRPC"],
    "cloud": ["AWS", "GCP", "Azure", "Docker", "Kubernetes"],
    "data_core": ["SQL", "Data Modeling", "ETL", "Data Warehousing"],
    "spark": ["Apache Spark", "PySpark", "Databricks"],
    "kafka": ["Kafka", "Streaming Pipelines"],
    "warehouse": ["Snowflake", "BigQuery", "Redshift"],
    "orchestration": ["Apache Airflow", "Orchestration"],
    "db": ["PostgreSQL", "MySQL", "MongoDB", "Redis"],
    "ml_core": ["Machine Learning", "Feature Engineering", "Model Evaluation"],
    "dl": ["PyTorch", "TensorFlow", "Deep Learning"],
    "nlp": ["NLP", "Transformers", "LLMs"],
    "cv": ["Computer Vision", "OpenCV"],
    "mlops": ["MLOps", "Model Monitoring", "Experiment Tracking"],
    "devops": ["Terraform", "Infrastructure as Code", "Observability", "SRE"],
    "security": ["AppSec", "Threat Modeling", "IAM", "OWASP", "Network Security"],
}

KEYWORD_TO_BUNDLES: List[Tuple[re.Pattern, List[str]]] = [
    (re.compile(r"\b(java|spring)\b", re.I), ["core_swe", "java", "cloud", "db"]),
    (re.compile(r"\b(python|fastapi|flask)\b", re.I), ["core_swe", "python", "cloud", "db"]),
    (re.compile(r"\b(react|frontend|ui|web)\b", re.I), ["core_swe", "js_frontend"]),
    (re.compile(r"\b(node|node\.js)\b", re.I), ["core_swe", "node", "js_frontend", "db"]),
    (re.compile(r"\b(golang|go)\b", re.I), ["core_swe", "go", "cloud", "db"]),
    (re.compile(r"\b(data engineer|etl|pipeline|analytics engineer|bi)\b", re.I),
     ["data_core", "warehouse", "orchestration", "db", "cloud"]),
    (re.compile(r"\b(spark|databricks)\b", re.I), ["data_core", "spark", "cloud"]),
    (re.compile(r"\b(kafka|stream)\b", re.I), ["data_core", "kafka", "cloud"]),
    (re.compile(r"\b(snowflake|bigquery|redshift)\b", re.I), ["data_core", "warehouse"]),
    (re.compile(r"\b(machine learning|ml engineer|ai engineer)\b", re.I), ["ml_core", "dl", "mlops", "cloud"]),
    (re.compile(r"\b(mlops)\b", re.I), ["mlops", "devops", "cloud"]),
    (re.compile(r"\b(nlp|llm|transformer)\b", re.I), ["ml_core", "dl", "nlp", "mlops"]),
    (re.compile(r"\b(computer vision|vision)\b", re.I), ["ml_core", "dl", "cv", "mlops"]),
    (re.compile(r"\b(devops|sre|reliability|platform)\b", re.I), ["devops", "cloud", "db"]),
    (re.compile(r"\b(cloud)\b", re.I), ["cloud", "devops"]),
    (re.compile(r"\b(security|appsec|infosec)\b", re.I), ["security", "cloud", "devops"]),
]

DEFAULT_BUNDLES = ["core_swe", "cloud", "db"]

SALARY_BANDS = {
    "Software/Platform": (90000, 185000),
    "Data": (95000, 190000),
    "ML/AI": (105000, 210000),
    "DevOps/SRE": (100000, 200000),
    "Security": (105000, 210000),
}

def role_family_from_title(title: str) -> str:
    t = title.lower()
    if "security" in t or "appsec" in t or "infosec" in t:
        return "Security"
    if "devops" in t or "sre" in t or "reliability" in t or "platform" in t:
        return "DevOps/SRE"
    if "machine learning" in t or "mlops" in t or re.search(r"\bml\b", t) or "ai" in t or "data scientist" in t:
        return "ML/AI"
    if "data" in t or "analytics" in t or "bi" in t:
        return "Data"
    return "Software/Platform"

def infer_bundles(text: str) -> List[str]:
    bundles: List[str] = []
    for pattern, mapped in KEYWORD_TO_BUNDLES:
        if pattern.search(text):
            bundles.extend(mapped)
    if not bundles:
        bundles = DEFAULT_BUNDLES.copy()
    seen = set()
    out = []
    for b in bundles:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out

def pick_skills(bundles: List[str]) -> List[str]:
    skills: List[str] = []
    for b in bundles:
        skills.extend(SKILL_CATALOG.get(b, []))
    skills = list(dict.fromkeys(skills))
    max_len = random.randint(10, 18)
    if len(skills) > max_len:
        skills = random.sample(skills, k=max_len)
    skills.sort()
    return skills

def make_title(level: str) -> str:
    fn = random.choice(FUNCTIONS)
    domain = random.choice(DOMAINS) if random.random() < 0.65 else ""
    tech = random.choice(TECH_MODIFIERS) if random.random() < 0.55 else ""
    prefix = random.choice(LEVEL_PREFIX[level]).strip()

    parts = [p for p in [prefix, tech, fn, f"({domain})" if domain else ""] if p and p.strip()]
    title = re.sub(r"\s{2,}", " ", " ".join(parts)).strip()
    return title

def sample_salary(family: str, level: str) -> Tuple[int, int]:
    lo, hi = SALARY_BANDS.get(family, (85000, 175000))
    mult = {"Entry": 0.85, "Mid": 1.00, "Senior": 1.18, "Staff": 1.35}[level]
    lo, hi = int(lo * mult), int(hi * mult)
    salary_min = random.randint(lo, max(lo + 5000, hi - 45000))
    salary_max = random.randint(max(salary_min + 12000, hi - 30000), hi)
    return salary_min, salary_max

def make_description(title: str, skills: List[str]) -> str:
    # Include synonyms so search works for "developer"/"engineer" both ways.
    synonyms = "engineer developer"
    core = ", ".join(skills[:6])
    return (
        f"We are hiring a {title} ({synonyms}) to build and scale production systems. "
        f"Key technologies include {core}. Own delivery, collaborate cross-functionally, ship reliably."
    )

def generate(n: int, seed: int) -> pd.DataFrame:
    random.seed(seed)
    np.random.seed(seed)
    Faker.seed(seed)

    now = datetime.now()
    rows = []

    for i in range(n):
        level = random.choices(LEVELS, weights=[0.18, 0.42, 0.30, 0.10], k=1)[0]
        title = make_title(level)
        family = role_family_from_title(title)

        company = random.choice(COMPANIES)
        loc, st = random.choice(US_CITIES)
        remote = bool(np.random.choice([True, False], p=[0.40, 0.60]))

        days_ago = int(np.random.choice(range(0, 45), p=np.linspace(1.8, 0.6, 45) / np.linspace(1.8, 0.6, 45).sum()))
        posted_date = (now - timedelta(days=days_ago)).date().isoformat()

        bundles = infer_bundles(title)
        skills = pick_skills(bundles)
        salary_min, salary_max = sample_salary(family, level)

        rows.append({
            "job_id": f"J{now.strftime('%Y%m%d')}-{i:05d}",
            "title": title,
            "role_family": family,
            "company": company,
            "location": loc,
            "state": st,
            "remote": remote,
            "is_remote": remote,
            "posted_date": posted_date,
            "experience_level": level,
            "salary_min": salary_min,
            "salary_max": salary_max,
            "salary_mid": int((salary_min + salary_max) / 2),
            "skills": "|".join(skills),
            "description": make_description(title, skills),
        })

    return pd.DataFrame(rows)

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=20000)
    parser.add_argument("--out", type=str, default="data/raw/jobs.csv")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    df = generate(args.n, args.seed)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    df.to_csv(args.out, index=False)
    print(f"✅ Generated {len(df):,} rows -> {args.out}")
    print(df.head(3).to_string(index=False))

if __name__ == "__main__":
    main()