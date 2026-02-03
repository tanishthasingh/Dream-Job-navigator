import streamlit as st
import time

def render():
    st.markdown("""
        <div style="text-align: center; padding: 50px 0;">
            <h1 style="font-size: 3.5rem; margin-bottom: 20px;">DreamJob Navigator</h1>
            <p style="font-size: 1.5rem; color: #666;">The GenAI-powered platform to accelerate your career growth worldwide.</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        with st.container(border=True):
            st.subheader("Start Your Journey")
            
            dream_job = st.text_input("What is your Dream Job?", placeholder="e.g. Senior DevOps Engineer")
            

            
            uploaded_file = st.file_uploader("Upload your Resume (PDF)", type="pdf")
            
            target_country = st.selectbox(
                "Target Country for Relocation",
                ["USA", "Canada", "Germany", "UK", "Australia", "UAE", "India"]
            )
            
            st.markdown("---")

            if st.button("Analyze Career Path", use_container_width=True, type="primary"):
                if dream_job and uploaded_file:
                    with st.spinner("Analyzing your profile..."):
                        # Save uploaded file temporarily or pass the file object directly if library supports it
                        # pypdf supports file-like objects
                        
                        try:
                            from services.career_analyzer import analyze_profile, extract_text_from_pdf
                            
                            # Debug: View what the system sees
                            raw_text = extract_text_from_pdf(uploaded_file)
                            uploaded_file.seek(0) # Reset pointer for the actual analysis
                            
                            with st.expander("🔍 Debug: Analysis Details (Recruiter won't see this)"):
                                st.write("**Extracted Text (first 500 chars):**")
                                st.code(raw_text[:500] + "...")
                                if not raw_text.strip():
                                    st.error("WARNING: No text was extracted from this PDF!")
                                
                            result = analyze_profile(dream_job, uploaded_file, target_country)
                            
                            if result.get("success"):
                                if "target_role_detected" in result:
                                    st.info(f"Detected Role: **{result['target_role_detected']}**")
                                
                                st.session_state.analysis_complete = True
                                st.session_state.analysis_result = result
                                st.session_state.user_job = dream_job
                                st.session_state.user_country = target_country
                                
                                # Save to DB using Authenticated Email
                                from services.db_handler import save_profile
                                user_email = st.session_state.get("user_email", "unknown_user")
                                if save_profile(user_email, result):
                                    st.toast("Progress saved to Cloud! ☁️")
                                
                                # Trigger navigation to Dashboard
                                st.session_state.manual_selection = "Dashboard"
                                st.success("Analysis Complete! Redirecting...")
                                time.sleep(1) # Give user a second to see the debug info if they want
                                st.rerun()
                            else:
                                st.error(f"Analysis failed: {result.get('error')}")
                        except Exception as e:
                            st.error(f"An error occurred: {str(e)}")
                            print(f"Analysis error: {e}")
                else:
                    st.error("Please provide both a Job Title and Resume.")
