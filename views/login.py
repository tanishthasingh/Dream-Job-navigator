import streamlit as st
import time
from services import db_handler

def render():
    st.markdown("""
        <div style="text-align: center; padding-top: 50px;">
            <h1>🔐 DreamJob Access</h1>
            <p>Login or Create an Account to save your career progress.</p>
        </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email Address", placeholder="you@example.com")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
                
                if submitted:
                    if not email or not password:
                        st.error("Please enter both email and password.")
                    else:
                        with st.spinner("Verifying credentials..."):
                            success, result = db_handler.verify_user(email.strip(), password)
                            if success:
                                st.success("Login Successful!")
                                # Set Session State
                                st.session_state.authenticated = True
                                st.session_state.user_email = email.strip()
                                st.session_state.analysis_result = result
                                if result:
                                    st.session_state.analysis_complete = True
                                    st.session_state.manual_selection = "Dashboard"
                                else:
                                    st.session_state.manual_selection = "Home"
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error(str(result))
        
        with tab2:
            st.warning("New users: Please sign up to create a secure profile.")
            with st.form("signup_form"):
                new_email = st.text_input("Email Address")
                new_pass = st.text_input("Choose Password", type="password", help="Make it strong!")
                confirm_pass = st.text_input("Confirm Password", type="password")
                submitted_signup = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted_signup:
                    if not new_email or not new_pass:
                        st.error("All fields are required.")
                    elif new_pass != confirm_pass:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating account..."):
                            success, msg = db_handler.create_user(new_email.strip(), new_pass)
                            if success:
                                st.success("Account Created! You can now Login.")
                            else:
                                st.error(msg)
