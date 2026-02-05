import pandas as pd

def fetch_jobs():
    data = [
        {'job_title': 'Software Engineer', 'required_skills': 'Python, SQL, AWS'},
        {'job_title': 'Data Engineer', 'required_skills': 'Python, Spark, SQL'},
        {'job_title': 'Software Engineer', 'required_skills': 'Java, Python, Docker'},
        {'job_title': 'Data Engineer', 'required_skills': 'SQL, Snowflake, Python'},
        {'job_title': 'Software Engineer', 'required_skills': 'Python, React, SQL'}
    ]
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Ingest script test:")
    print(fetch_jobs())