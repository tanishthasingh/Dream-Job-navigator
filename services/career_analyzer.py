import pypdf
import json
import re

def extract_text_from_pdf(file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = pypdf.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return ""

def get_job_skills_database():
    """Returns a dictionary of job roles and their typical required skills."""
    return {
        "DevOps Engineer": {
            "critical": ["Linux", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Git", "AWS", "Azure", "Python", "Bash"],
            "nice_to_have": ["Terraform", "Ansible", "Prometheus", "Grafana", "Go", "Ruby"]
        },
        "Software Engineer": {
            "critical": ["Python", "Java", "JavaScript", "SQL", "Git", "Data Structures", "Algorithms", "REST API"],
            "nice_to_have": ["React", "Node.js", "Docker", "AWS", "GraphQL", "NoSQL"]
        },
        "Data Scientist": {
            "critical": ["Python", "SQL", "Pandas", "NumPy", "Scikit-learn", "Machine Learning", "Statistics"],
            "nice_to_have": ["TensorFlow", "PyTorch", "Spark", "Hadoop", "AWS", "Visualization"]
        },
        "Product Manager": {
            "critical": ["Product Strategy", "Agile", "Scrum", "User Research", "Roadmapping", "Communication"],
            "nice_to_have": ["SQL", "Data Analysis", "Jira", "Figma", "Marketing"]
        },
        # Default fallback
        "General": {
            "critical": ["Communication", "Problem Solving", "Teamwork", "Time Management", "Adaptability"],
            "nice_to_have": ["Leadership", "Project Management", "Creativity"]
        }
    }

def analyze_profile(job_title, resume_file, country):
    """
    Analyzes the resume against the target job title using keyword matching.
    """
    resume_text = extract_text_from_pdf(resume_file)
    if not resume_text:
        return {"error": "Could not extract text from resume. Please ensure it is a valid PDF."}
    
    # Normalize text
    resume_text_lower = resume_text.lower()
    
    # Determine which skill set to use
    db = get_job_skills_database()
    # Simple fuzzy match for job title, default to General if no match
    target_role = "General"
    best_match_len = 0
    
    for role in db.keys():
        if role.lower() in job_title.lower():
            # Basic longest match win (e.g. choose specific over general)
            if len(role) > best_match_len:
                target_role = role
                best_match_len = len(role)
            
    required_skills = db[target_role]["critical"]
    nice_to_have_skills = db[target_role]["nice_to_have"]
    
    missing_skills_list = []
    matched_skills_count = 0
    total_critical_skills = len(required_skills)
    
    # Check for critical skills
    for skill in required_skills:
        # Use regex for word boundary matching to avoid partial matches (e.g. "Go" in "Good")
        # Creating a safe regex pattern
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, resume_text_lower):
            matched_skills_count += 1
        else:
            missing_skills_list.append({"skill": skill, "severity": "High"})
            
    # Check for nice-to-have skills
    for skill in nice_to_have_skills:
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if not re.search(pattern, resume_text_lower):
            missing_skills_list.append({"skill": skill, "severity": "Medium"})

    # Calculate Score
    if total_critical_skills > 0:
        raw_score = (matched_skills_count / total_critical_skills) * 100
        # normalize to be a bit more generous
        match_score = int(min(raw_score + 10, 95)) 
    else:
        match_score = 70
        
    # Aggregate all relevant skills for the Matrix
    # Combine (Matched Critical + Missing Critical + Missing Nice-to-have)
    # Actually simpler: Just take the Target Role's Critical Skills + Nice To Have
    all_required_skills = []
    
    # Add Critical Skills
    for skill in required_skills:
        status = "Completed"
        # Re-check match logic simply or check if in missing list (inverse)
        is_missing = any(m['skill'] == skill for m in missing_skills_list)
        if is_missing:
            status = "To Do"
        
        all_required_skills.append({
            "Skill": skill,
            "Category": "Technical",
            "Priority": "High",
            "Status": status
        })
        
    # Add Nice to Have
    for skill in nice_to_have_skills:
        status = "Completed"
        is_missing = any(m['skill'] == skill for m in missing_skills_list)
        if is_missing:
            status = "To Do"
            
        all_required_skills.append({
            "Skill": skill,
            "Category": "Technical",
            "Priority": "Medium",
            "Status": status
        })

    # Salary Ranges (Mock data enhanced with basic logic)
    base_salaries = {
        "USA": [90000, 160000],
        "Canada": [75000, 130000],
        "Germany": [65000, 110000],
        "UK": [55000, 100000],
        "Australia": [80000, 140000],
        "UAE": [100000, 150000],
        "India": [500000, 2500000] # INR
    }
    salary_range = base_salaries.get(country, [50000, 100000])
    
    # Adjust salary slightly based on score
    salary_multiplier = 0.9 + (match_score / 200) # 0.9 to 1.4
    adjusted_salary_range = [int(s * salary_multiplier) for s in salary_range]

    # Get dynamic companies
    hiring_companies = get_companies_by_region_and_role(country, target_role)
    
    # Generate dynamic roadmap
    roadmap = generate_roadmap(missing_skills_list)

    return {
        "success": True,
        "match_score": match_score,
        "missing_skills": missing_skills_list,
        "all_required_skills": all_required_skills, # New field for Matrix
        "job_title": job_title,
        "target_country": country,
        "salary_range": adjusted_salary_range,
        "market_demand_score": 85, 
        "hiring_companies": hiring_companies,
        "roadmap": roadmap
    }

def get_companies_by_region_and_role(country, role):
    """
    Returns a curated list of companies based on research for specific regions.
    """
    # Normalized role to simple categories
    role_cat = "General"
    if "devops" in role.lower() or "cloud" in role.lower() or "sre" in role.lower():
        role_cat = "DevOps"
    elif "software" in role.lower() or "developer" in role.lower() or "engineer" in role.lower():
        role_cat = "SWE"
    elif "data" in role.lower():
        role_cat = "Data"
        
    companies_db = {
        "USA": {
            "DevOps": ["Google", "Amazon (AWS)", "Netflix", "Datadog", "HashiCorp", "Cloudflare", "Snowflake"],
            "SWE": ["Google", "Meta", "Microsoft", "Stripe", "Airbnb", "Uber", "Salesforce"],
            "Data": ["Databricks", "Palantir", "Snowflake", "Google DeepMind", "OpenAI", "Meta"]
        },
        "Germany": {
            "DevOps": ["SAP", "Siemens", "Zalando", "Adidas", "BMW Group", "Cloudflare", "Personio"],
            "SWE": ["SAP", "Zalando", "N26", "Delivery Hero", "HelloFresh", "SoundCloud", "Wirecard"],
            "Data": ["SAP", "Celonis", "Zalando", "BMW", "Allianz", "Bayer"]
        },
        "Canada": {
            "DevOps": ["Shopify", "RBC", "Telus", "BlackBerry", "OpenText", "Hootsuite"],
            "SWE": ["Shopify", "Wealthsimple", "Lightspeed", "Clio", "Constellation Software", "CGI"],
            "Data": ["Shopify", "Cohere", "Layer 6 AI", "Element AI", "BMO", "TD Bank"]
        },
        "UK": {
            "DevOps": ["Revolut", "Monzo", "Deliveroo", "Barclays", "Sky", "Arm", "Ocado Technology"],
            "SWE": ["DeepMind", "Revolut", "Monzo", "Wise", "Improbable", "Darktrace"],
            "Data": ["DeepMind", "Revolut", "Starling Bank", "AstraZeneca", "HSBC"]
        },
        "Australia": {
            "DevOps": ["Atlassian", "Canva", "Telstra", "Commonwealth Bank", "Xero", "Afterpay"],
            "SWE": ["Atlassian", "Canva", "Xero", "WiseTech Global", "REA Group", "SafetyCulture"],
            "Data": ["Canva", "Atlassian", "Macquarie Group", "Telstra", "Woolworths Group"]
        },
        "UAE": {
            "DevOps": ["Careem", "Talabat", "Noon", "Etisalat", "G42", "Emirates Group"],
            "SWE": ["Careem", "Dubizzle", "Property Finder", "Kitopi", "BitOasis", "Tabby"],
            "Data": ["G42", "Careem", "Noon", "Etisalat", "Dubai Digital Authority"]
        },
        "India": {
            "DevOps": ["TCS", "Infosys", "Wipro", "HCLTech", "Accenture India", "Zoho", "Freshworks"],
            "SWE": ["Google India", "Microsoft India", "Flipkart", "Swiggy", "Zomato", "Paytm", "Ola", "PhonePe"],
            "Data": ["Mu Sigma", "Fractal Analytics", "Tiger Analytics", "Flipkart", "InMobi", "Paytm"]
        }
    }
    
    # Fallback to general tech giants if country not explicit or role distinct
    defaults = ["Google", "Amazon", "Microsoft", "IBM", "Oracle", "Accenture"]
    
    country_data = companies_db.get(country, {})
    role_companies = country_data.get(role_cat, defaults)
    
    # Return formatted list WITHOUT simulated openings to ensure factual accuracy
    import random
    formatted_companies = []
    
    # Pick a subset or all
    selected = role_companies[:8] # Show top 8
    if len(role_companies) > 8:
        selected = random.sample(role_companies, k=8)
    
    for comp in selected:
        formatted_companies.append({
            "Company": comp,
            "Location": country,
            "Type": "Top Employer"
        })
        
    return formatted_companies

def generate_roadmap(missing_skills):
    """
    Generates a dynamic 2-3 quarter detailed roadmap based on missing skills.
    """
    roadmap = []
    import datetime
    
    # Current Quarter
    today = datetime.date.today()
    q = (today.month - 1) // 3 + 1
    current_q_str = f"{today.year}-Q{q}"
    
    # Phase 1: Analysis & Fundamentals
    roadmap.append({
        "Stage": "Phase 1: Foundation & Analysis", 
        "Status": "Computed", 
        "Date": current_q_str,
        "Topics": ["Profile Gap Analysis", "Resume Keyword Optimization", "Market Research"],
        "Action": "Review identified skill gaps and update resume."
    })
    
    # Prepare Skill-Topic Mapping
    skill_topics = {
        "Kubernetes": ["Container Orchestration", "Pods & Services", "Deployments", "Helm Charts", "Ingress Controllers"],
        "Docker": ["Containerization", "Dockerfiles", "Multi-stage Builds", "Docker Compose", "Networking"],
        "AWS": ["EC2 & S3", "IAM Roles", "VPC Networking", "Lambda Serverless", "CloudWatch"],
        "CI/CD": ["Pipeline as Code", "GitHub Actions / Jenkins", "Automated Testing", "Blue/Green Deployment"],
        "Python": ["Scripting", "Automation Libraries (boto3)", "API Development (FastAPI/Flask)", "Data Structures"],
        "Linux": ["Shell Scripting", "File System Permissions", "Process Management", "Networking commands (curl, netstat)"],
        "Terraform": ["IaC Concepts", "State Management", "Modules", "Providers"],
        "SQL": ["Joins", "Indexing", "Normalization", "Transactions"],
        "React": ["Components", "Hooks", "State Management (Redux/Context)", "Router"]
    }
    
    if not missing_skills:
        # Maintenance / Job Hunt Mode
        roadmap.append({
            "Stage": "Phase 2: Interview Readiness", 
            "Status": "In Progress", 
            "Date": current_q_str,
            "Topics": ["System Design Mock Interviews", "Behavioral Questions (STAR)", "LeetCode/HackerRank"],
            "Action": "Schedule 3 mock interviews this month."
        })
        roadmap.append({
            "Stage": "Phase 3: Active Application", 
            "Status": "Pending", 
            "Date": "Next Quarter",
            "Topics": ["Networking on LinkedIn", "Salary Negotiation", "Company Research"],
            "Action": "Apply to 5 high-intent companies per week."
        })
    else:
        # Distribute missing skills
        high_pri = [s['skill'] for s in missing_skills if s['severity'] == 'High']
        med_pri = [s['skill'] for s in missing_skills if s['severity'] == 'Medium']
        
        # Quarter 1: Focus on High Impact
        next_q = q + 1
        year = today.year
        if next_q > 4:
            next_q = 1
            year += 1
            
        topics_q1 = []
        focused_skills = high_pri[:3] if high_pri else med_pri[:3]
        
        for skill in focused_skills:
            # Get specific sub-topics or default generic ones
            subs = skill_topics.get(skill, [f"{skill} Fundamentals", f"{skill} Advanced Patterns"])
            topics_q1.extend(subs[:2]) # Add top 2 sub-topics
            
        roadmap.append({
            "Stage": "Phase 2: Core Skill Build", 
            "Status": "Pending", 
            "Date": f"{year}-Q{next_q}",
            "Topics": topics_q1[:5], # Limit to 5 bullets
            "Action": f"Build a capstone project using {', '.join(focused_skills[:2])}."
        })
        
        # Quarter 2: Specialization
        next_next_q = next_q + 1
        year_next = year
        if next_next_q > 4:
            next_next_q = 1
            year_next += 1
            
        topics_q2 = []
        secondary_skills = high_pri[3:] + med_pri
        if not secondary_skills:
            secondary_skills = ["System Design", "Cloud Architecture"] # Fillers
            
        for skill in secondary_skills[:3]:
            subs = skill_topics.get(skill, [f"{skill} Mastery", f"{skill} Best Practices"])
            topics_q2.extend(subs[:2])

        roadmap.append({
            "Stage": "Phase 3: Deep Dive & Certifications", 
            "Status": "Future", 
            "Date": f"{year_next}-Q{next_next_q}",
            "Topics": topics_q2[:5],
            "Action": "Obtain relevant certification (e.g., CKA, AWS Solution Architect)."
        })
        
    return roadmap
