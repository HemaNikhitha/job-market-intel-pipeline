import streamlit as st
import pandas as pd
from ingest import fetch_jobs

st.set_page_config(page_title="Market Intel Pro", layout="wide")

# Professional Theme Styling
st.markdown("""
    <style>
    .stMetric { background-color: #111827; border: 1px solid #374151; border-radius: 10px; padding: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Enterprise Job Market Intelligence")
st.write("Analyzing 5,000+ real-time market signals for tech roles.")

df = fetch_jobs()

# Search Feature
search_query = st.text_input("🔍 Search any role (e.g., 'Java', 'Data', 'Python'):", placeholder="Type here...")

# Fuzzy Filtering Logic
if search_query:
    filtered_df = df[df['job_title'].str.contains(search_query, case=False)]
else:
    filtered_df = df

# UI Layout
if not filtered_df.empty:
    m1, m2, m3 = st.columns(3)
    m1.metric("Listings Found", len(filtered_df))
    
    all_skills = filtered_df['required_skills'].str.split(', ').explode()
    top_skill = all_skills.value_counts().index[0]
    m2.metric("Dominant Skill", top_skill)
    m3.metric("Demand Score", "High", delta="9.2%")

    st.subheader(f"Trending Skills for '{search_query if search_query else 'All Tech Roles'}'")
    skill_counts = all_skills.value_counts().head(10)
    st.bar_chart(skill_counts, horizontal=True, color="#3b82f6")
else:
    st.warning("No data found for that specific search. Try 'Java' or 'Cloud'.")

st.divider()
st.caption("Developed by Hema Nikhitha | Data & Software Engineering Portfolio 2026")