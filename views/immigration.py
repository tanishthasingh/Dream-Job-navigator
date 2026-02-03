import streamlit as st

def render():
    st.title("Global Mobility & Visa Intelligence")
    st.markdown("Verified visa pathways for tech professionals. *Data based on official 2024/2025 government fee schedules.*")
    
    # Factual Data Dictionary (Sourced Feb 2026)
    visa_db = {
        "USA": {
            "Visa": "H-1B Specialty Occupation",
            "Official_Link": "https://www.uscis.gov/working-in-the-united-states/h-1b-specialty-occupations",
            "Fees": "$460 (Petition) + $2,805 (Premium Processing - Optional)",
            "Timeline": "Electronic Registration: March. Selection: April. Start Date: Oct 1.",
            "Processing_Time": "Regular: 8-10 months | Premium: 15 days",
            "Requirements": ["Bachelor's Degree", "Job Offer from US Employer", "Employer Selection in Lottery"],
            "Pros": "Dual intent (path to Green Card)",
            "Cons": "Lottery based (approx 25% selection chance)"
        },
        "Germany": {
            "Visa": "EU Blue Card (Germany)",
            "Official_Link": "https://www.make-it-in-germany.com/en/visa-residence/types/eu-blue-card",
            "Fees": "€100 (Issuance fee)",
            "Timeline": "Apply anytime upon receiving contract.",
            "Processing_Time": "4-6 weeks (varies by embassy)",
            "Requirements": ["German Recognized Degree", "Job Offer with Salary > €45,300 (Bottleneck Professions 2024)"],
            "Pros": "Fast track to PR (21 months with B1 German)",
            "Cons": "Strict salary thresholds"
        },
        "Canada": {
            "Visa": "Express Entry (Federal Skilled Worker)",
            "Official_Link": "https://www.canada.ca/en/immigration-refugees-citizenship/services/immigrate-canada/express-entry.html",
            "Fees": "$1,365 CAD (Processing) + $515 CAD (RPRF) = ~$1,880 CAD",
            "Timeline": "Draws occur every 2 weeks.",
            "Processing_Time": "Standard: 6 months",
            "Requirements": ["CRS Score cutoff", "ECA Report", "IELTS/CELPIP Language Test"],
            "Pros": "Direct Permanent Residence (PR)",
            "Cons": "High CRS score competition (>500 points recently)"
        },
        "UK": {
            "Visa": "Skilled Worker Visa",
            "Official_Link": "https://www.gov.uk/skilled-worker-visa",
            "Fees": "£719 (up to 3 years) + Immigration Health Surcharge (£1,035/year)",
            "Timeline": "Apply up to 3 months before work start.",
            "Processing_Time": "3 weeks (Outside UK) | 8 weeks (Inside UK)",
            "Requirements": ["Sponsorship from licensed employer", "Job in eligible list", "Salary > £38,700 (standard rate April 2024)"],
            "Pros": "Flexible 5-year route to ILR",
            "Cons": "High IHS fees and salary threshold increase"
        },
        "UAE": {
            "Visa": "Green Visa (Freelance/Skilled)",
            "Official_Link": "https://u.ae/en/information-and-services/visa-and-emirates-id/residence-visas/residence-visa-for-working-in-the-uae/green-visa",
            "Fees": "~AED 2,500 + Medical/ID fees",
            "Timeline": "Apply anytime.",
            "Processing_Time": "5-10 working days",
            "Requirements": ["Bachelor's Degree", "Salary > AED 15,000/month", "Valid Employment Contract"],
            "Pros": "Self-sponsored for 5 years. No employer dependence.",
            "Cons": "No path to citizenship."
        },
        "Australia": {
            "Visa": "Skills in Demand (Subclass 482)",
            "Official_Link": "https://immi.homeaffairs.gov.au/visas/getting-a-visa/visa-listing/temporary-skill-shortage-482",
            "Fees": "AUD 3,210 (Medium-term) / AUD 1,495 (Short-term)",
            "Timeline": "Requires employer nomination first.",
            "Processing_Time": "Specilist: 7 days | Core Skills: 21-47 days",
            "Requirements": ["Experience > 2 years", "English Proficiency (IELTS 5.0+)", "Nomination by Approved Sponsor"],
            "Pros": "Pathway to PR (186 ENS) after 2 years.",
            "Cons": "High cost of living and sponsorship dependency."
        }
    }
    
    selected_c = st.selectbox("Select Target Country", list(visa_db.keys()))
    
    info = visa_db[selected_c]
    
    st.subheader(f"🇺🇳 {selected_c}: {info['Visa']}")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**💰 Official Fees:**\n\n {info['Fees']}")
        st.markdown(f"**⏱️ Processing Time:**\n\n {info['Processing_Time']}")
        
    with c2:
        st.markdown(f"**📋 Mandatory Requirements:**")
        for req in info['Requirements']:
            st.markdown(f"- {req}")
            
    st.info(f"👉 **Verify at Official Source:** [{info['Official_Link']}]({info['Official_Link']})")
    
    with st.expander("Show detailed Pros & Cons"):
        col_p, col_c = st.columns(2)
        col_p.success(f"**Pros:** {info['Pros']}")
        col_c.error(f"**Cons:** {info['Cons']}")
