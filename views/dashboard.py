import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from utils.data import get_job_market_data, get_skill_gap_data, get_roadmap_data

def render():
    st.title(f"Career Dashboard: {st.session_state.get('user_job', 'DevOps Engineer')}")
    
    # Key Metrics Row
    analysis_result = st.session_state.get('analysis_result')
    
    # Use real data if available, otherwise fallback to mock data
    if analysis_result:
        market_score = analysis_result.get('market_demand_score', 85)
        match_score = analysis_result.get('match_score', 0)
        missing_skills = analysis_result.get('missing_skills', [])
        salary_range = analysis_result.get('salary_range', [0, 0])
        country = analysis_result.get('target_country', st.session_state.get('user_country', 'USA'))
        hiring_companies = analysis_result.get('hiring_companies', [])
    else:
        # Fallback to mock data
        market = get_job_market_data()
        skills = get_skill_gap_data()
        market_score = market['demand_score']
        match_score = skills['match_score']
        missing_skills = skills['missing_skills']
        salary_range = market['salary_ranges'].get(st.session_state.get('user_country', 'USA'), [0,0])
        country = st.session_state.get('user_country', 'USA')
        hiring_companies = market['hiring_companies']

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.metric("Market Demand Score", f"{market_score}/100", "+5% vs last month")
    with c2:
        st.metric("Skill Match", f"{match_score}%", f"{len(missing_skills)} Missing Skills")
    with c3:
        avg_salary = sum(salary_range)/2 if salary_range else 0
        st.metric("Potential Salary (Avg)", f"${avg_salary:,.0f}", country)

    st.markdown("---")

    # Gauges and Charts
    col_left, col_right = st.columns([1, 1])

    with col_left:
        st.subheader("Skill Match Gauge")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = match_score,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Match Score"},
            gauge = {'axis': {'range': [None, 100]},
                     'bar': {'color': "#4a90e2"},
                     'steps' : [
                         {'range': [0, 50], 'color': "lightgray"},
                         {'range': [50, 80], 'color': "gray"}],
                     'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 90}}))
        st.plotly_chart(fig, use_container_width=True)
        
        st.subheader("Missing Skills Analysis")
        for skill in missing_skills:
            color = "red" if skill['severity'] == "High" else "orange" if skill['severity'] == "Medium" else "green"
            st.markdown(f"""
                <div style="margin-bottom: 10px; padding: 10px; border-left: 5px solid {color}; background-color: rgba(0,0,0,0.05);">
                    <strong>{skill['skill']}</strong> <span style="float: right; color: {color};">{skill['severity']} Priority</span>
                </div>
            """, unsafe_allow_html=True)

    with col_right:
        st.subheader("Salary Comparison by Country")
        # Transform salary data for Plotly - Keeping this part simpler for now, maybe just show current country vs others from static data if needed
        # For now, let's just visualize the current range vs a few others from static data for context
        
        static_market = get_job_market_data() # For comparison context
        data = []
        
        # Add current user analysis
        data.append({"Country": country + " (You)", "Min": salary_range[0], "Max": salary_range[1], "Avg": sum(salary_range)/2})
        
        # Add a few others for comparison
        for c, r in static_market['salary_ranges'].items():
            if c != country:
                data.append({"Country": c, "Min": r[0], "Max": r[1], "Avg": sum(r)/2})
        
        df_sal = pd.DataFrame(data[:5]) # Top 5 to avoid crowding
        fig_sal = px.bar(df_sal, x='Country', y='Avg', color='Avg', 
                         title="Average Annual Salary (USD)",
                         color_continuous_scale='Viridis')
        st.plotly_chart(fig_sal, use_container_width=True)
        
        if "UAE" in country:
            st.info("💡 Note: UAE offers tax-free salaries. Companies often provide relocation packages.")
        
        st.subheader("Top Hiring Companies")
        st.dataframe(hiring_companies, use_container_width=True)
        
        # Live Search Link
        search_query = f"{st.session_state.get('user_job', 'simulated')} jobs in {country}"
        search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_query.replace(' ', '%20')}"
        st.link_button("🔎 Search Live Jobs on LinkedIn", search_url, type="secondary", use_container_width=True)

    st.markdown("---")
    st.subheader("Personalized Career Roadmap")
    
    roadmap = analysis_result.get('roadmap', get_roadmap_data()) # Fallback if missing
    
    st.subheader("Personalized Career Roadmap")
    
    roadmap = analysis_result.get('roadmap', get_roadmap_data()) # Fallback if missing
    
    # Detailed Vertical/Card Timeline
    for item in roadmap:
        status_color = "#4caf50" if item.get('Status') == "Computed" or item.get('Status') == "Completed" else "#2196f3" if "Progress" in item.get('Status', '') else "#ff9800"
        
        with st.container():
            st.markdown(f"""
            <div style="border-left: 4px solid {status_color}; padding-left: 20px; margin-bottom: 20px;">
                <h4 style="margin: 0;">{item.get('Stage')} <span style="font-size: 0.8rem; background: {status_color}; color: white; padding: 2px 8px; border-radius: 10px; margin-left: 10px;">{item.get('Date')}</span></h4>
                <p style="color: #666; margin-bottom: 5px;"><em>{item.get('Status', 'Pending')}</em></p>
                <div style="margin-top: 10px;">
                    <strong>🎯 Focus Topics:</strong>
                    <ul style="margin-top: 5px;">
                        {''.join([f'<li>{t}</li>' for t in item.get('Topics', [])])}
                    </ul>
                </div>
                <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>⚡ Action Item:</strong> {item.get('Action', 'Complete relevant learning modules.')}
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- PERSISTENT DEBUG SECTION ---
    if analysis_result and "debug_info" in analysis_result:
        st.markdown("---")
        with st.expander("🛠️ Analysis Debug Information (Developer Only)"):
            d = analysis_result["debug_info"]
            st.write(f"**Detected Role:** {analysis_result.get('target_role_detected', 'N/A')}")
            st.write(f"**Role Match Score:** {d.get('role_match_score', 0)}")
            st.write(f"**Tokens Matched for Role:** {', '.join(d.get('tokens_found', []))}")
            st.write("**Extracted Text Snippet (First 1000 chars):**")
            st.code(d.get("raw_text_snippet", "No text found"))
            if not d.get("raw_text_snippet", "").strip():
                st.error("🚨 CRITICAL: No text was extracted from this resume. The PDF might be an image/scanned or encrypted.")
            
            st.info("💡 If the result is wrong, please share a screenshot of this box with me!")
