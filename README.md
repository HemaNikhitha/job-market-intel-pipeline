# 🛰️ Tech Skill Radar
**An enterprise-grade radar and intelligence pipeline analyzing 5,000+ job market signals.**

[🚀 View Live Dashboard](https://tech-skill-radar.streamlit.app)

---

## 📈 Overview
Tech Skill Radar is a role-agnostic intelligence tool designed to bridge the gap between job seekers and market demand. By processing high-volume synthetic job data, it identifies trending skills, salary benchmarks, and remote-work shifts across Software Engineering, Data, DevOps, and Security disciplines.

## 🛠️ Key Features
* **Fuzzy Search Intelligence:** Multi-keyword filtering allows for deep-dive analysis into specific niches (e.g., "ML Engineer" or "Backend Developer").
* **Real-Time Skill Discovery:** Automatically extracts and ranks the top 15 observed skills for any filtered search.
* **Salary & Remote Benchmarking:** Provides instant median salary calculations and remote-work percentage based on 5,000+ records.
* **Direct LinkedIn Integration:** One-click "Apply" links generated dynamically for every filtered job result.

## ⚙️ Tech Stack
* **Language:** Python 3.12
* **Frontend:** Streamlit (Custom UI with metric cards and interactive dataframes)
* **Data Processing:** Pandas (High-performance filtering and aggregation)
* **Deployment:** Streamlit Community Cloud with automated GitHub sync

## 🚀 Installation & Local Usage
1. Clone the repo: `git clone https://github.com/HemaNikhitha/job-market-intel-pipeline.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run dashboard.py`