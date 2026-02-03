import streamlit as st
import pandas as pd

def render():
    st.title("Skills Progress Matrix")
    
    st.info("Track your proficiency in key technical and soft skills needed for your Dream Job. This matrix updates based on your inputs.")
    
    # Initialize session state for progress if not exists
    if "skill_matrix" not in st.session_state:
        # Build initial matrix from analysis if available
        analysis = st.session_state.get("analysis_result", {})
        
        # New Logic: Get comprehensive skill list from analysis
        matrix_data = []
        
        if "all_required_skills" in analysis:
            # Use the detailed breakdown we just added to analyzer
            for s in analysis["all_required_skills"]:
                matrix_data.append({
                    "Skill": s["Skill"],
                    "Category": s["Category"],
                    "Done": True if s["Status"] == "Completed" else False,
                    "Priority": s["Priority"]
                })
        else:
            # Fallback (Legacy or if analysis failed)
            default_skills = ["Python", "Docker", "Kubernetes", "AWS", "CI/CD", "Communication", "System Design"]
            missing = [s['skill'] for s in analysis.get("missing_skills", [])]
            
            for skill in default_skills:
                is_missing = skill in missing
                matrix_data.append({
                    "Skill": skill, 
                    "Category": "Technical" if skill not in ["Communication", "Leadership"] else "Soft Skills",
                    "Done": False if is_missing else True, 
                    "Priority": "High"
                })
            
        st.session_state.skill_matrix = pd.DataFrame(matrix_data)

    # Allow adding new skills
    with st.expander("Add Custom Skill"):
        c1, c2, c3 = st.columns([2, 1, 1])
        new_skill = c1.text_input("Skill Name")
        new_cat = c2.selectbox("Category", ["Technical", "Soft Skills", "Language"])
        if c3.button("Add"):
            if new_skill:
                new_row = {"Skill": new_skill, "Category": new_cat, "Done": False, "Priority": "Medium"}
                st.session_state.skill_matrix = pd.concat([st.session_state.skill_matrix, pd.DataFrame([new_row])], ignore_index=True)
                st.rerun()

    # Editable Dataframe
    edited_df = st.data_editor(
        st.session_state.skill_matrix,
        column_config={
            "Done": st.column_config.CheckboxColumn(
                "Completed?",
                help="Check to mark as done",
                default=False,
            ),
            "Priority": st.column_config.SelectboxColumn(
                "Priority",
                options=["High", "Medium", "Low"],
                required=True,
            ),
        },
        disabled=["Skill", "Category"],
        use_container_width=True,
        num_rows="dynamic",
        key="matrix_editor"
    )
    
    # Update state
    if not edited_df.equals(st.session_state.skill_matrix):
        st.session_state.skill_matrix = edited_df
        st.rerun()

    # Metrics
    if not edited_df.empty:
        # Calculate completion from boolean checkbox
        completed = edited_df["Done"].sum()
        total = len(edited_df)
        progress = completed / total
        
        st.write("### Overall Readiness")
        st.progress(progress)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Skills", total)
        c2.metric("Completed", completed)
        c3.metric("Remaining", total - completed)
        
        if progress == 1.0:
            st.balloons()
            st.success("You are ready for your Dream Job!")
