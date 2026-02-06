#!/usr/bin/env python3
"""
dashboard.py
Job Market Intelligence dashboard with:
- Synonym-aware search (developer ~ engineer, SWE/SDE, etc.)
- Soft matching (avoids strict AND returning 0 too often)
- Recommended skills always derived from query
"""

from __future__ import annotations

import os
import re
from collections import Counter
from datetime import datetime
from typing import List, Tuple

import altair as alt
import pandas as pd
import streamlit as st

DATA_PATH = os.getenv("JOB_DATA_PATH", "data/raw/jobs.csv")

# Query -> recommended skills (still used)
KEYWORD_SKILLS: List[Tuple[re.Pattern, List[str]]] = [
    (re.compile(r"\b(java|spring)\b", re.I),
     ["Java", "Spring Boot", "Microservices", "REST APIs", "JPA/Hibernate", "Unit Testing", "CI/CD", "AWS"]),
    (re.compile(r"\b(python|fastapi|flask)\b", re.I),
     ["Python", "FastAPI", "Flask", "REST APIs", "SQL", "Docker", "CI/CD"]),
    (re.compile(r"\b(react|frontend|ui)\b", re.I),
     ["React", "TypeScript", "JavaScript", "HTML", "CSS", "Testing", "API Integration"]),
    (re.compile(r"\b(node|node\.js)\b", re.I),
     ["Node.js", "Express.js", "REST APIs", "SQL", "Redis", "Docker", "CI/CD"]),
    (re.compile(r"\b(golang|go)\b", re.I),
     ["Golang", "gRPC", "Microservices", "System Design", "Docker", "Kubernetes"]),
    (re.compile(r"\b(data engineer|etl|pipeline|warehous|analytics engineer|bi)\b", re.I),
     ["SQL", "ETL", "Data Modeling", "Airflow", "Spark", "Kafka", "Snowflake/BigQuery", "AWS/GCP"]),
    (re.compile(r"\b(spark|databricks)\b", re.I),
     ["Apache Spark", "PySpark", "Databricks", "SQL", "Delta Lake"]),
    (re.compile(r"\b(kafka|stream)\b", re.I),
     ["Kafka", "Streaming Pipelines", "Spark", "Schema Design", "Monitoring"]),
    (re.compile(r"\b(snowflake|bigquery|redshift)\b", re.I),
     ["Snowflake/BigQuery/Redshift", "SQL", "Data Warehousing", "dbt (optional)"]),
    (re.compile(r"\b(machine learning|ml engineer|ai engineer)\b", re.I),
     ["Machine Learning", "Feature Engineering", "Model Evaluation", "PyTorch/TensorFlow", "MLOps", "Docker"]),
    (re.compile(r"\b(mlops)\b", re.I),
     ["MLOps", "Model Monitoring", "Experiment Tracking", "Docker", "Kubernetes", "CI/CD"]),
    (re.compile(r"\b(nlp|llm|transformer)\b", re.I),
     ["NLP", "Transformers", "LLMs", "PyTorch", "Evaluation", "MLOps"]),
    (re.compile(r"\b(devops|sre|site reliability|platform)\b", re.I),
     ["CI/CD", "Docker", "Kubernetes", "Terraform", "Observability", "SRE", "AWS/GCP/Azure"]),
    (re.compile(r"\b(security|appsec|infosec)\b", re.I),
     ["AppSec", "Threat Modeling", "IAM", "OWASP", "Cloud Security", "Network Security"]),
]

DEFAULT_RECOMMENDED = ["Git", "SQL", "CI/CD", "Docker", "Cloud Basics", "System Design"]

# Synonym replacements for search normalization
SYNONYMS = {
    "developer": "engineer",
    "programmer": "engineer",
    "swe": "software engineer",
    "sde": "software engineer",
    "backend": "backend engineer",
    "front-end": "frontend",
    "front end": "frontend",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "devops": "devops",
}

def normalize_query(q: str) -> str:
    q = (q or "").strip().lower()
    # apply phrase-level synonyms
    for k, v in SYNONYMS.items():
        q = re.sub(rf"\b{re.escape(k)}\b", v, q)
    # collapse spaces
    q = re.sub(r"\s{2,}", " ", q).strip()
    return q

def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", (text or "").lower())

def soft_match(series: pd.Series, query: str) -> pd.Series:
    """
    Soft match:
    - if 1 token: must match it
    - if 2-3 tokens: require >=2 matches
    - if 4+ tokens: require >=3 matches
    """
    q = normalize_query(query)
    toks = tokenize(q)
    if not toks:
        return pd.Series([True] * len(series), index=series.index)

    s = series.fillna("").str.lower()
    needed = 1
    if len(toks) in (2, 3):
        needed = 2
    elif len(toks) >= 4:
        needed = 3

    hit_count = pd.Series([0] * len(series), index=series.index)
    for t in toks:
        hit_count += s.str.contains(re.escape(t), regex=True).astype(int)

    return hit_count >= needed

def parse_skills(pipe: str) -> List[str]:
    if not isinstance(pipe, str) or not pipe:
        return []
    return [x.strip() for x in pipe.split("|") if x.strip()]

def top_skills(df: pd.DataFrame, k: int = 15) -> pd.DataFrame:
    counter = Counter()
    for s in df["skills"].fillna(""):
        counter.update(parse_skills(s))
    top = counter.most_common(k)
    return pd.DataFrame(top, columns=["skill", "count"])

def recommended_skills_from_query(query: str) -> List[str]:
    q = normalize_query(query)
    if not q:
        return DEFAULT_RECOMMENDED
    rec: List[str] = []
    for pattern, skills in KEYWORD_SKILLS:
        if pattern.search(q):
            rec.extend(skills)
    if not rec:
        rec = DEFAULT_RECOMMENDED.copy()
    seen = set()
    out = []
    for s in rec:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out[:18]

def fmt_money(x: float) -> str:
    return f"${int(x):,}"

def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Run:\n  python ingest.py --n 20000 --out {path}\n"
        )
    df = pd.read_csv(path)
    df["posted_date"] = pd.to_datetime(df["posted_date"], errors="coerce")
    df["is_remote"] = df.get("is_remote", df.get("remote", False)).astype(bool)
    return df

# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Job Market Intelligence", page_icon="📊", layout="wide")
st.title("Real-Time Job Market Intelligence")
st.caption("Type any tech role. Search is synonym-aware + soft-matched to avoid empty results.")

df = load_data(DATA_PATH)

with st.sidebar:
    st.header("Search & Filters")

    query = st.text_input(
        "Search roles (works for ANY role text)",
        placeholder="e.g., software developer, senior java, data engineer etl, cloud security",
    )

    role_families = ["All"] + sorted(df["role_family"].dropna().unique().tolist())
    role_choice = st.selectbox("Role family", role_families, index=0)

    exp_levels = ["All"] + sorted(df["experience_level"].dropna().unique().tolist())
    exp_choice = st.selectbox("Experience level", exp_levels, index=0)

    remote_choice = st.selectbox("Remote", ["All", "Remote only", "Onsite/Hybrid only"], index=0)

    states = ["All"] + sorted(df["state"].dropna().unique().tolist())
    state_choice = st.selectbox("State", states, index=0)

    st.divider()
    topk = st.slider("Top observed skills", 10, 30, 15, 1)
    st.caption("Tip: If you get 0 matches, loosen filters first (Role family/State/Remote).")

# Search across title + description for broader hit rate
search_space = (df["title"].fillna("") + " " + df["description"].fillna(""))
mask = soft_match(search_space, query)

if role_choice != "All":
    mask &= df["role_family"].eq(role_choice)
if exp_choice != "All":
    mask &= df["experience_level"].eq(exp_choice)
if remote_choice == "Remote only":
    mask &= df["is_remote"].eq(True)
elif remote_choice == "Onsite/Hybrid only":
    mask &= df["is_remote"].eq(False)
if state_choice != "All":
    mask &= df["state"].eq(state_choice)

filtered = df.loc[mask].copy()

recommended = recommended_skills_from_query(query)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total jobs", f"{len(df):,}")
c2.metric("Matched jobs", f"{len(filtered):,}")

if len(filtered) > 0:
    c3.metric("Median salary (mid)", fmt_money(filtered["salary_mid"].median()))
    c4.metric("Remote share", f"{(filtered['is_remote'].mean() * 100):.0f}%")
else:
    c3.metric("Median salary (mid)", "—")
    c4.metric("Remote share", "—")

st.divider()

st.subheader("Recommended skills for your search")
st.caption("Inferred from your query text — always works (even if no jobs match).")
st.write(" • ".join(recommended))

st.divider()

left, right = st.columns([1.1, 1.0])

with left:
    st.subheader("Observed top skills (from matched jobs)")
    if len(filtered) == 0:
        st.info("No matching jobs with current filters. Loosen filters (State/Remote/Role family) to see observed skills.")
        skills_df = top_skills(df, k=topk)
        st.caption("Fallback: showing global skill frequency from the entire dataset.")
    else:
        skills_df = top_skills(filtered, k=topk)

    bar = (
        alt.Chart(skills_df)
        .mark_bar()
        .encode(
            x=alt.X("count:Q", title="Mentions"),
            y=alt.Y("skill:N", sort="-x", title="Skill"),
            tooltip=["skill:N", "count:Q"],
        )
        .properties(height=520)
    )
    st.altair_chart(bar, use_container_width=True)

with right:
    st.subheader("Postings over time")
    if len(filtered) > 0 and filtered["posted_date"].notna().any():
        ts = (
            filtered.dropna(subset=["posted_date"])
            .groupby(filtered["posted_date"].dt.date)
            .size()
            .reset_index(name="count")
            .rename(columns={"posted_date": "date"})
        )
        line = (
            alt.Chart(ts)
            .mark_line(point=True)
            .encode(
                x=alt.X("date:T", title="Date"),
                y=alt.Y("count:Q", title="Postings"),
                tooltip=["date:T", "count:Q"],
            )
            .properties(height=260)
        )
        st.altair_chart(line, use_container_width=True)
    else:
        st.info("No time-series data for the current filters.")

    st.subheader("Role family split")
    if len(filtered) > 0:
        split = filtered["role_family"].value_counts().reset_index()
        split.columns = ["role_family", "count"]
        pie = (
            alt.Chart(split)
            .mark_arc()
            .encode(
                theta="count:Q",
                color="role_family:N",
                tooltip=["role_family:N", "count:Q"],
            )
            .properties(height=260)
        )
        st.altair_chart(pie, use_container_width=True)
    else:
        st.info("No matched roles to split.")

st.divider()

st.subheader("Matched job results")

show_cols = [
    "job_id", "title", "role_family", "experience_level",
    "company", "location", "is_remote",
    "salary_min", "salary_max", "salary_mid",
    "posted_date", "skills",
]

out = filtered.copy()
if "posted_date" in out.columns:
    out["posted_date"] = out["posted_date"].dt.date.astype(str)

if len(out) == 0:
    st.info("No rows to display. Try removing State/Role family filters or searching broader: 'software', 'engineer', 'developer'.")
else:
    out["salary_min"] = out["salary_min"].apply(lambda x: f"${int(x):,}")
    out["salary_max"] = out["salary_max"].apply(lambda x: f"${int(x):,}")
    out["salary_mid"] = out["salary_mid"].apply(lambda x: f"${int(x):,}")
    out["is_remote"] = out["is_remote"].apply(lambda x: "Remote" if x else "Onsite/Hybrid")
    st.dataframe(out[show_cols], use_container_width=True, height=420)

st.caption(f"Dataset: {DATA_PATH} | Rendered: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")