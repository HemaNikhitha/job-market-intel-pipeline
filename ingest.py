import pandas as pd
import random

def fetch_jobs():
    # Large pool of roles and skills for a "Real-World" feel
    all_roles = [
        "Java Developer", "Python Engineer", "Data Scientist", "ML Engineer",
        "DevOps Architect", "Cloud Engineer", "Frontend Specialist", 
        "Backend Developer", "Full Stack Engineer", "Systems Analyst"
    ]
    
    # Mapping keywords to logical skills
    skill_map = {
        "java": ["Java", "Spring Boot", "Hibernate", "Maven", "Oracle"],
        "python": ["Python", "Django", "Flask", "Pandas", "NumPy"],
        "data": ["SQL", "Snowflake", "Spark", "Airflow", "Tableau"],
        "ml": ["PyTorch", "TensorFlow", "Scikit-Learn", "Minitab", "R"],
        "cloud": ["AWS", "Azure", "GCP", "Terraform", "Docker"],
        "frontend": ["React", "JavaScript", "HTML/CSS", "TypeScript", "Next.js"]
    }

    data = []
    # Scaled to 5,000 for high-volume analysis
    for _ in range(5000):
        role = random.choice(all_roles)
        # Determine skills based on role keywords
        role_lower = role.lower()
        assigned_skills = []
        
        for key, skills in skill_map.items():
            if key in role_lower:
                assigned_skills.extend(random.sample(skills, 3))
        
        # Fallback if no keyword matches
        if not assigned_skills:
            assigned_skills = ["Communication", "Problem Solving", "Agile"]

        data.append({
            'job_title': role,
            'required_skills': ", ".join(list(set(assigned_skills)))
        })
    
    return pd.DataFrame(data)