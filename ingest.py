import pandas as pd
import random

def fetch_jobs():
    # Define professional role categories and their logical skills
    categories = {
        "Software Engineer": ["Java", "Python", "Spring Boot", "Docker", "AWS", "SQL", "Microservices"],
        "Data Engineer": ["Python", "SQL", "Spark", "Snowflake", "Airflow", "ETL", "Redshift"],
        "ML Engineer": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "Minitab", "Pandas", "MLOps"],
        "DevOps Engineer": ["Terraform", "Kubernetes", "Jenkins", "AWS", "Linux", "Ansible", "CI/CD"],
        "Frontend Developer": ["React", "TypeScript", "Tailwind", "Next.js", "JavaScript", "HTML/CSS"]
    }
    
    data = []
    # Generate 1,000 logical records
    for _ in range(1000):
        # Pick a random category
        role = random.choice(list(categories.keys()))
        # Pick 4-5 skills specifically from THAT category's list
        skills = random.sample(categories[role], random.randint(4, 5))
        
        data.append({
            'job_title': role,
            'required_skills': ", ".join(skills)
        })
    
    return pd.DataFrame(data)