#!/usr/bin/env python3
"""
dashboard.py (Professional / Classy UI)
- Synonym-aware search + soft matching
- Recommended skills always computed
- Enterprise-style layout: header bar, metric cards, tabs, styled sidebar, clean charts
- Shareable URL query params + Download CSV + LinkedIn apply links
- Hides Streamlit chrome (menu/deploy/footer) for a polished public demo
"""

from __future__ import annotations

import os
import re
from collections import Counter
from datetime import datetime
from typing import List, Tuple
from urllib.parse import urlencode, quote_plus

import altair as alt
import pandas as pd
import streamlit as st

DATA_PATH = os.getenv("JOB_DATA_PATH", "data/raw/jobs.csv")

# -----------------------------
# Recommended skills mapping
# -----------------------------
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

SYNONYMS = {
    "developer": "engineer",
    "programmer": "engineer",
    "swe": "software engineer",
    "sde": "software engineer",
    "front end": "frontend",
    "front-end": "frontend",
    "ml": "machine learning",
    "ai": "artificial intelligence",
}

# -----------------------------
# Styling (CSS)
# -----------------------------
def inject_css() -> None:
    st.markdown(
        """
<style>
.stApp {
  background: radial-gradient(1200px 600px at 30% 10%, rgba(99,102,241,0.18), transparent 55%),
              radial-gradient(1000px 550px at 70% 15%, rgba(16,185,129,0.12), transparent 60%),
              linear-gradient(180deg, #0b1220 0%, #060a14 100%);
  color: #e7eaf0;
}
.block-container { padding-top: 1.2rem; padding-bottom: 2.2rem; }
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg, rgba(255,255,255,0.03), rgba(255,255,255,0.01));
  border-right: 1px solid rgba(255,255,255,0.06);
}

/* Hide Streamlit chrome for clean public demo */
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; } /* hides deploy/menu area */

.headerbar {
  padding: 18px 18px;
  border: 1px solid rgba(255,255,255,0.08);
  background: rgba(255,255,255,0.03);
  border-radius: 18px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.35);
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap; /* prevents title from cutting */
}
.brand { display: flex; flex-direction: column; gap: 4px; min-width: 260px; }
.brand-title {
  font-size: 26px;
  font-weight: 800;
  letter-spacing: 0.2px;
  line-height: 1.15;
  word-break: break-word;
}
.brand-subtitle { font-size: 13px; opacity: 0.78; }

.badge {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid rgba(255,255,255,0.10);
  background: rgba(255,255,255,0.04);
  opacity: 0.92;
}

.card {
  padding: 16px 16px;
  border-radius: 18px;
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.08);
  box-shadow: 0 12px 30px rgba(0,0,0,0.35);
}
.card-title { font-size: 12px; opacity: 0.78; margin-bottom: 6px; }
.card-value { font-size: 24px; font-weight: 800; }
.card-hint  { font-size: 12px; opacity: 0.72; margin-top: 4px; }

.pills { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.pill {
  font-size: 12px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(99,102,241,0.14);
  border: 1px solid rgba(99,102,241,0.25);
}

div[data-testid="stDataFrame"] {
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid rgba(255,255,255,0.08);
}
</style>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Helpers
# -----------------------------
def normalize_query(q: str) -> str:
    q = (q or "").strip().lower()
    for k, v in SYNONYMS.items():
        q = re.sub(rf"\b{re.escape(k)}\b", v, q)
    q = re.sub(r"\s{2,}", " ", q).strip()
    return q

def build_share_url(base_url: str, params: dict) -> str:
    clean = {k: v for k, v in params.items() if v not in (None, "", "All")}
    return f"{base_url}?{urlencode(clean)}" if clean else base_url

def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-z0-9]+", (text or "").lower())

def soft_match(series: pd.Series, query: str) -> pd.Series:
    q = normalize_query(query)
    toks = tokenize(q)
    if not toks:
        return pd.Series([True] * len(series), index=series.index)

    needed = 1
    if len(toks) in (2, 3):
        needed = 2
    elif len(toks) >= 4:
        needed = 3

    s = series.fillna("").str.lower()
    hit_count = pd.Series([0] * len(series), index=series.index)
    for t in toks:
        hit_count += s.str.contains(re.escape(t), regex=True).astype(int)
    return hit_count >= needed

def parse_skills(pipe: str) -> List[str]:
    if not isinstance(pipe, str) or not pipe:
        return []
    return [x.strip() for x in pipe.split("|") if x.strip()]

def top_skills(df_: pd.DataFrame, k: int = 15) -> pd.DataFrame:
    counter = Counter()
    for s in df_["skills"].fillna(""):
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

def build_linkedin_jobs_link(title: str, company: str, location: str) -> str:
    """
    LinkedIn Jobs search URL. Works well for demo + feels professional.
    """
    # LinkedIn search is forgiving; include title + company + location
    keywords = f"{title} {company}".strip()
    loc = (location or "").strip()

    # This format is stable:
    # https://www.linkedin.com/jobs/search/?keywords=...&location=...
    return (
        "https://www.linkedin.com/jobs/search/?"
        + urlencode({"keywords": keywords, "location": loc})
    )

@st.cache_data(show_spinner=False)
def load_data(path: str) -> pd.DataFrame:
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"Dataset not found at '{path}'. Run:\n  python ingest.py --n 20000 --out {path}\n"
        )
    df_ = pd.read_csv(path)
    df_["posted_date"] = pd.to_datetime(df_["posted_date"], errors="coerce")
    df_["is_remote"] = df_.get("is_remote", df_.get("remote", False)).astype(bool)
    return df_

# -----------------------------
# App
# -----------------------------
st.set_page_config(page_title="Job Market Intelligence", page_icon="📊", layout="wide")
inject_css()

df = load_data(DATA_PATH)

# Shareable links: compatibility-safe
try:
    qp = st.query_params
    qp_query = qp.get("q", "")
    qp_role = qp.get("role", "All")
    qp_level = qp.get("level", "All")
    qp_remote = qp.get("remote", "All")
    qp_state = qp.get("state", "All")
except Exception:
    qp_query, qp_role, qp_level, qp_remote, qp_state = "", "All", "All", "All", "All"

# Header
st.markdown(
    f"""
<div class="headerbar">
  <div class="brand">
    <div class="brand-title">Job Market Intelligence</div>
    <div class="brand-subtitle">Search any tech role → recommended skills + observed market signals</div>
  </div>
  <div class="badge">Dataset: {len(df):,} jobs • Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
</div>
""",
    unsafe_allow_html=True,
)
st.write("")

# Sidebar filters
with st.sidebar:
    st.header("Search & Filters")

    query = st.text_input(
        "Role / keywords",
        value=qp_query,
        placeholder="software developer, senior java, data engineer etl, cloud security, mlops",
    )

    role_families = ["All"] + sorted(df["role_family"].dropna().unique().tolist())
    role_choice = st.selectbox(
        "Role family",
        role_families,
        index=role_families.index(qp_role) if qp_role in role_families else 0,
    )

    exp_levels = ["All"] + sorted(df["experience_level"].dropna().unique().tolist())
    exp_choice = st.selectbox(
        "Experience level",
        exp_levels,
        index=exp_levels.index(qp_level) if qp_level in exp_levels else 0,
    )

    remote_opts = ["All", "Remote only", "Onsite/Hybrid only"]
    remote_choice = st.selectbox(
        "Remote",
        remote_opts,
        index=remote_opts.index(qp_remote) if qp_remote in remote_opts else 0,
    )

    states = ["All"] + sorted(df["state"].dropna().unique().tolist())
    state_choice = st.selectbox(
        "State",
        states,
        index=states.index(qp_state) if qp_state in states else 0,
    )

    st.divider()
    topk = st.slider("Top observed skills", 10, 30, 15, 1)

# Filter logic
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

# Write query params back (shareable)
try:
    st.query_params.update({
        "q": query,
        "role": role_choice,
        "level": exp_choice,
        "remote": remote_choice,
        "state": state_choice,
    })
except Exception:
    pass

recommended = recommended_skills_from_query(query)

# KPI cards
total_jobs = f"{len(df):,}"
matched_jobs = f"{len(filtered):,}"

if len(filtered) > 0:
    median_salary = fmt_money(filtered["salary_mid"].median())
    remote_share = f"{(filtered['is_remote'].mean() * 100):.0f}%"
    hint = "Filtered market slice"
else:
    median_salary = "—"
    remote_share = "—"
    hint = "Loosen filters to see matches"

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""<div class="card"><div class="card-title">Total Jobs</div><div class="card-value">{total_jobs}</div><div class="card-hint">Synthetic dataset</div></div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""<div class="card"><div class="card-title">Matched Jobs</div><div class="card-value">{matched_jobs}</div><div class="card-hint">{hint}</div></div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""<div class="card"><div class="card-title">Median Salary (Mid)</div><div class="card-value">{median_salary}</div><div class="card-hint">Based on matches</div></div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""<div class="card"><div class="card-title">Remote Share</div><div class="card-value">{remote_share}</div><div class="card-hint">Within matched set</div></div>""", unsafe_allow_html=True)

st.write("")

# Share link card
base_url = "http://localhost:8502"
share_url = build_share_url(base_url, {
    "q": query,
    "role": role_choice,
    "level": exp_choice,
    "remote": remote_choice,
    "state": state_choice,
})
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Share this view")
st.code(share_url, language="text")
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# Tabs
tab1, tab2, tab3 = st.tabs(["Overview", "Skills Intel", "Job Results"])

with tab1:
    st.subheader("Recommended skills for your search")
    pills_html = "".join([f'<span class="pill">{s}</span>' for s in recommended])
    st.markdown(f'<div class="card"><div class="pills">{pills_html}</div></div>', unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.1, 1.0])

    with left:
        st.subheader("Observed top skills")
        skills_df = top_skills(filtered if len(filtered) > 0 else df, k=topk)

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
            donut = (
                alt.Chart(split)
                .mark_arc(innerRadius=70)
                .encode(
                    theta="count:Q",
                    color=alt.Color("role_family:N", legend=alt.Legend(title="Role Family")),
                    tooltip=["role_family:N", "count:Q"],
                )
                .properties(height=260)
            )
            st.altair_chart(donut, use_container_width=True)
        else:
            st.info("No matched roles to split.")

with tab2:
    st.subheader("Skills Intel")
    base_df = filtered if len(filtered) > 0 else df
    skills_df = top_skills(base_df, k=topk)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.altair_chart(
        alt.Chart(skills_df).mark_bar().encode(
            x=alt.X("count:Q", title="Mentions"),
            y=alt.Y("skill:N", sort="-x", title="Skill"),
            tooltip=["skill:N", "count:Q"],
        ).properties(height=520),
        use_container_width=True
    )
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.subheader("Matched Job Results")

    show_cols = [
        "job_id", "title", "role_family", "experience_level",
        "company", "location", "is_remote",
        "salary_min", "salary_max", "salary_mid",
        "posted_date", "skills",
        "apply_link",
    ]

    out = filtered.copy()

    # LinkedIn Jobs search link per row (professional)
    out["apply_link"] = out.apply(
        lambda r: build_linkedin_jobs_link(
            str(r.get("title", "")),
            str(r.get("company", "")),
            str(r.get("location", "")),
        ),
        axis=1,
    )

    if "posted_date" in out.columns:
        out["posted_date"] = pd.to_datetime(out["posted_date"], errors="coerce").dt.date.astype(str)

    if len(out) == 0:
        st.info("No rows to display. Broaden filters or try a simpler query like 'engineer'.")
    else:
        out["salary_min"] = out["salary_min"].apply(lambda x: f"${int(x):,}")
        out["salary_max"] = out["salary_max"].apply(lambda x: f"${int(x):,}")
        out["salary_mid"] = out["salary_mid"].apply(lambda x: f"${int(x):,}")
        out["is_remote"] = out["is_remote"].apply(lambda x: "Remote" if x else "Onsite/Hybrid")

        csv_bytes = out[show_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download matched jobs (CSV)",
            data=csv_bytes,
            file_name="matched_jobs.csv",
            mime="text/csv",
        )

        st.dataframe(
            out[show_cols],
            use_container_width=True,
            height=520,
            column_config={
                "apply_link": st.column_config.LinkColumn(
                    "Apply / View on LinkedIn",
                    help="Opens LinkedIn Jobs search for this title + company + location",
                    display_text="Open",
                )
            },
        )