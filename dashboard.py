import streamlit as st
import pandas as pd
from ingest import fetch_jobs

st.set_page_config(page_title="Market Intelligence", layout="wide")

# Custom Styling for a "Classy" look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1f2937; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Real-Time Job Market Intelligence")
st.info("Enter a role like 'ML Engineer', 'Data Engineer', or 'Software Engineer' to see trending skills.")

df = fetch_jobs()

# Sidebar Search
st.sidebar.header("Intelligence Filter")
search_query = st.sidebar.text_input("Search Job Title:", placeholder="e.g. ML Engineer")

# Filter logic
if search_query:
    filtered_df = df[df['job_title'].str.contains(search_query, case=False)]
else:
    filtered_df = df

# Dashboard UI
col1, col2 = st.columns([1, 2])

with col1:
    st.metric("Total Listings Found", len(filtered_df))
    if not filtered_df.empty:
        all_skills = filtered_df['required_skills'].str.split(', ').explode()
        top_skill = all_skills.value_counts().index[0]
        st.subheader(f"Top Skill: {top_skill}")
    else:
        st.error("No results found. Try a broader search!")

with col2:
    if not filtered_df.empty:
        skill_counts = all_skills.value_counts().head(10)
        st.bar_chart(skill_counts, horizontal=True)

st.divider()
st.caption("Data Architecture by Hema Nikhitha | Built for 2026 Job Market Trends")