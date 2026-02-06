# 🛰️ Tech Skill Radar
**An enterprise-grade radar and intelligence pipeline analyzing 5,000+ data signals.**

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://tech-skill-radar.streamlit.app)

Tech Skill Radar is a scalable data pipeline and interactive dashboard designed to bridge the gap between job seekers and market demand. It identifies trending skills, salary benchmarks, and remote-work shifts across the entire tech landscape.

---

## 🚀 Quick Start
No installation required. You can access the live intelligence engine immediately:
1. **Visit the Dashboard:** [tech-skill-radar.streamlit.app](https://tech-skill-radar.streamlit.app)
2. **Search a Role:** Type any role (e.g., "Data Engineer" or "DevOps") into the sidebar.
3. **Analyze:** Explore real-time skill rankings, median salaries, and direct application links.

---

## 🛠️ How It Works (The Pipeline)
This project follows a professional Data Engineering lifecycle:

1. **Data Ingestion:** A Python-based engine processes 5,000+ synthetic job records with role-specific skill mapping.
2. **Fuzzy Search Intelligence:** Uses advanced string matching to allow for flexible role discovery across various tech families.
3. **Aggregation Engine:** Pandas-driven logic calculates real-time metrics for salary (Mid/Senior levels) and remote-work availability.
4. **Interactive Visualization:** A custom Streamlit UI renders dynamic "Skill Intel" cards and application tracking tables.

---

## 🧩 Architecture
* **Language:** `Python 3.12`
* **Data Core:** `Pandas` (High-performance filtering & aggregation)
* **Interface:** `Streamlit` (Reactive UI components)
* **Deployment:** `CI/CD` via GitHub & Streamlit Cloud

---

## 💻 Local Development
If you wish to contribute or run this pipeline locally:

```bash
# Clone the repository
git clone [https://github.com/HemaNikhitha/job-market-intel-pipeline.git](https://github.com/HemaNikhitha/job-market-intel-pipeline.git)

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run dashboard.py