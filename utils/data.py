import pandas as pd
import datetime

def get_job_market_data():
    return {
        "demand_score": 85,
        "salary_ranges": {
            "USA": [80000, 150000],
            "Germany": [60000, 100000],
            "Canada": [70000, 120000],
            "UK": [50000, 90000],
            "Australia": [75000, 130000],
            "UAE": [90000, 140000] # Tax free hint
        },
        "hiring_companies": [
            {"Company": "Google", "Openings": 12, "Location": "Multiple"},
            {"Company": "Amazon", "Openings": 8, "Location": "Remote"},
            {"Company": "Microsoft", "Openings": 15, "Location": "Redmond"},
            {"Company": "StartUp Inc", "Openings": 3, "Location": "Berlin"}
        ]
    }

def get_skill_gap_data():
    return {
        "match_score": 65,
        "missing_skills": [
            {"skill": "Kubernetes", "severity": "High"},
            {"skill": "GraphQL", "severity": "Medium"},
            {"skill": "System Design", "severity": "High"},
            {"skill": "Terraform", "severity": "Low"}
        ],
        "recommended_certs": [
            "CKA (Certified Kubernetes Administrator)",
            "AWS Certified Solutions Architect"
        ]
    }

def get_roadmap_data():
    return [
        {"Stage": "Foundations", "Status": "Completed", "Date": "2024-Q1"},
        {"Stage": "Advanced Dev", "Status": "In Progress", "Date": "2024-Q3"},
        {"Stage": "System Design", "Status": "Pending", "Date": "2025-Q1"},
        {"Stage": "Leadership", "Status": "Pending", "Date": "2025-Q4"}
    ]

def get_learning_resources():
    return [
        {
            "title": "Kubernetes for the Absolute Beginners",
            "provider": "Udemy",
            "type": "Paid",
            "duration": "5h",
            "rating": 4.7,
            "link": "#",
            "tags": ["Kubernetes", "DevOps"]
        },
        {
            "title": "Google Cloud Skills Boost",
            "provider": "Google",
            "type": "Free",
            "duration": "Self-paced",
            "rating": 4.8,
            "link": "#",
            "tags": ["Cloud", "GCP"]
        },
        {
            "title": "System Design Primer",
            "provider": "GitHub",
            "type": "Free",
            "duration": "Reading",
            "rating": 4.9,
            "link": "#",
            "tags": ["System Design"]
        },
        {
            "title": "AWS Solutions Architect Associate",
            "provider": "AWS SkillBuilder",
            "type": "Certification",
            "duration": "20h",
            "rating": 4.6,
            "link": "#",
            "tags": ["AWS", "Cloud"]
        }
    ]

def get_immigration_data():
    return {
        "Canada": {
            "visa": "Express Entry (FSW)",
            "eligibility": "Points based (Age, Ed, Exp, Lang)",
            "fees": "~$1,365 CAD",
            "timeline": "6-12 months",
            "pr_pathway": "Direct PR upon selection"
        },
        "Germany": {
            "visa": "Opportunity Card / Blue Card",
            "eligibility": "Degree + Salary threshold or Points",
            "fees": "€100",
            "timeline": "3-6 months",
            "pr_pathway": "After 21-33 months"
        },
        "USA": {
            "visa": "H-1B / O-1",
            "eligibility": "Sponsorship / Extraordinary Ability",
            "fees": "$460+",
            "timeline": "Lottery based / Variable",
            "pr_pathway": "Green Card (Backlogged for some)"
        },
         "UK": {
            "visa": "Skilled Worker Visa",
            "eligibility": "Job Offer + Sponsorship",
            "fees": "£625 - £1,423",
            "timeline": "3-8 weeks",
            "pr_pathway": "After 5 years"
        }
    }
