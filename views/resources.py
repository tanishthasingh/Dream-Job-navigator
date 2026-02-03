import streamlit as st

def render():
    st.title("Personalized Learning Resources")
    st.markdown("Curated, high-quality resources to bridge your skill gaps. Direct links to official documentation and top-rated courses.")
    
    # Factual Resource Database (No estimates, verified top providers)
    resources_db = {
        "Kubernetes": [
            {"title": "Kubernetes Official Docs", "link": "https://kubernetes.io/docs/home/", "type": "Documentation", "cost": "Free"},
            {"title": "Certified Kubernetes Administrator (CKA)", "link": "https://training.linuxfoundation.org/certification/certified-kubernetes-administrator-cka/", "type": "Certification", "cost": "Paid"},
            {"title": "Kubernetes for the Absolute Beginners (Udemy)", "link": "https://www.udemy.com/course/learn-kubernetes/", "type": "Course", "cost": "Paid"}
        ],
        "Docker": [
            {"title": "Docker Get Started", "link": "https://docs.docker.com/get-started/", "type": "Documentation", "cost": "Free"},
            {"title": "Docker Mastery: with Kubernetes +Swarm (Udemy)", "link": "https://www.udemy.com/course/docker-mastery/", "type": "Course", "cost": "Paid"}
        ],
        "AWS": [
            {"title": "AWS Skill Builder", "link": "https://explore.skillbuilder.aws/", "type": "Course", "cost": "Freemium"},
            {"title": "AWS Certified Solutions Architect - Associate", "link": "https://aws.amazon.com/certification/certified-solutions-architect-associate/", "type": "Certification", "cost": "Paid"}
        ],
        "Python": [
            {"title": "Python.org Official Tutorial", "link": "https://docs.python.org/3/tutorial/", "type": "Documentation", "cost": "Free"},
            {"title": "Automate the Boring Stuff with Python", "link": "https://automatetheboringstuff.com/", "type": "Book/Course", "cost": "Free"}
        ],
        "CI/CD": [
            {"title": "GitLab CI/CD Docs", "link": "https://docs.gitlab.com/ee/ci/", "type": "Documentation", "cost": "Free"},
            {"title": "Jenkins - The Definitive Guide", "link": "https://www.jenkins.io/doc/", "type": "Documentation", "cost": "Free"}
        ],
        "System Design": [
            {"title": "System Design Primer (GitHub)", "link": "https://github.com/donnemartin/system-design-primer", "type": "Guide", "cost": "Free"},
            {"title": "Grokking the System Design Interview", "link": "https://www.designgurus.io/course/grokking-the-system-design-interview", "type": "Course", "cost": "Paid"}
        ]
    }
    
    # Get user skills context
    analysis = st.session_state.get("analysis_result", {})
    missing_skills = [s['skill'] for s in analysis.get("missing_skills", [])]
    
    # Display logic
    if not missing_skills:
        # Default view if no analysis
        categories = resources_db.keys()
    else:
        # Prioritize missing skills
        categories = list(set(missing_skills)) + [k for k in resources_db.keys() if k not in missing_skills]
    
    for category in categories:
        # Simple fuzzy matching for our DB keys
        db_key = None
        for k in resources_db.keys():
            if k.lower() in category.lower() or category.lower() in k.lower():
                db_key = k
                break
        
        if db_key:
            with st.expander(f"📚 {db_key} Resources", expanded=True if category in missing_skills else False):
                for item in resources_db[db_key]:
                    c1, c2, c3 = st.columns([3, 1, 1])
                    c1.markdown(f"**[{item['title']}]({item['link']})**")
                    c2.caption(item['type'])
                    c3.caption(f"{item['cost']}")
