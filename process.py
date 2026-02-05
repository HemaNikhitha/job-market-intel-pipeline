from ingest import fetch_jobs
from collections import Counter

def main():
    print("--- Starting Data Processing ---")
    df = fetch_jobs()
    
    # Check if we got data
    if df.empty:
        print("Error: No data found!")
        return

    # Extract and count skills
    all_skills = []
    for skills_str in df['required_skills']:
        skills_list = [s.strip() for s in skills_str.split(',')]
        all_skills.extend(skills_list)
    
    counts = Counter(all_skills)
    
    print("Top 5 Skills Found:")
    for skill, count in counts.most_common(5):
        print(f"{skill}: {count}")
    print("--- Processing Complete ---")

if __name__ == "__main__":
    main()