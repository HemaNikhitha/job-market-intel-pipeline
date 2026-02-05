import pandas as pd
from datetime import datetime, timedelta

def fetch_jobs():
    data = [
        {
            'job_title': 'Software Engineer',
            'company': 'TechCorp',
            'required_skills': 'Python,SQL,Git',
            'posted_date': (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Data Engineer',
            'company': 'DataWorks',
            'required_skills': 'Python,Spark,Hadoop',
            'posted_date': (datetime.today() - timedelta(days=2)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Software Engineer',
            'company': 'InnovateX',
            'required_skills': 'Java,Spring,REST',
            'posted_date': (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Data Engineer',
            'company': 'AnalyticsPro',
            'required_skills': 'Scala,SQL,Airflow',
            'posted_date': (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Software Engineer',
            'company': 'WebSolutions',
            'required_skills': 'JavaScript,React,Node.js',
            'posted_date': (datetime.today() - timedelta(days=5)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Data Engineer',
            'company': 'BigData Inc',
            'required_skills': 'Python,ETL,Redshift',
            'posted_date': (datetime.today() - timedelta(days=6)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Software Engineer',
            'company': 'CloudNet',
            'required_skills': 'Go,AWS,Docker',
            'posted_date': (datetime.today() - timedelta(days=7)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Data Engineer',
            'company': 'Insightful',
            'required_skills': 'Python,SQL,Tableau',
            'posted_date': (datetime.today() - timedelta(days=8)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Software Engineer',
            'company': 'AppDev',
            'required_skills': 'C#,Azure,CI/CD',
            'posted_date': (datetime.today() - timedelta(days=9)).strftime('%Y-%m-%d')
        },
        {
            'job_title': 'Data Engineer',
            'company': 'DataMinds',
            'required_skills': 'Python,NoSQL,Kafka',
            'posted_date': (datetime.today() - timedelta(days=10)).strftime('%Y-%m-%d')
        }
    ]
    df = pd.DataFrame(data)
    return df