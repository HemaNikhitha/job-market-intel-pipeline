# 🛰️ Tech Skill Radar
**An enterprise-grade radar and intelligence pipeline analyzing 5,000+ data signals.**

[![Live Demo](https://img.shields.io/badge/Demo-Live%20on%20Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://tech-skill-radar.streamlit.app)

Tech Skill Radar is a scalable data pipeline and interactive dashboard designed to bridge the gap between job seekers and market demand. It identifies trending skills, salary benchmarks, and remote-work shifts across the entire tech landscape.

---

## ⚡ Live Exploration
Explore the live intelligence engine in three simple steps:
1. **Launch:** Open the [Tech Skill Radar](https://tech-skill-radar.streamlit.app).
2. **Filter:** Enter any tech role (e.g., "Full Stack Developer").
3. **Analyze:** Instantly view matched job counts, median salaries, and top skills.

---

## ⚙️ Technical Architecture:
This project implements a robust, end-to-end data lifecycle designed for high-performance market analysis.

1. **DataSynthesis & Ingestion:** Engineered a Python-based generation engine to simulate a high-cardinality dataset of 5,000+ job records, ensuring realistic attribute distribution for role types and seniority levels.
2. **Fuzzy Search Intelligence:** Implemented advanced string-matching logic to provide "Synonym-Aware" search capabilities, allowing the system to accurately categorize diverse job titles into unified role families.
3. **Vectorised Aggregation:** Leveraged the Pandas library for high-speed data manipulation, executing complex filtering and multi-dimensional aggregations (salary medians, remote-work ratios) in sub-second response times.
4. **Reactive Visualization:** Developed a dynamic UI using Streamlit that utilizes state management to provide real-time updates to KPI cards and interactive Plotly charts based on user-defined parameters.

---

## ---

---

## 🛠️ The Tech Stack
This project is built on a modern data stack optimized for scalability and performance.

| Layer | Technology | Role in Pipeline |
| :--- | :--- | :--- |
| **Language** | `Python 3.12` | Core logic and data processing engine |
| **Data Engine** | `Pandas` | High-performance vectorized filtering & aggregation |
| **Interface** | `Streamlit` | Reactive UI for real-time market visualization |
| **Deployment** | `CI/CD` | Automated sync via GitHub & Streamlit Cloud |

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