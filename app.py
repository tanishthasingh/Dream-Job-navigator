import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os
from PIL import Image

# Page config
st.set_page_config(
    page_title="DreamJob Navigator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

try:
    local_css("styles/style.css")
except FileNotFoundError:
    pass # Handle case where style might be missing temporarily

# Session State Initialization
if "analysis_complete" not in st.session_state:
    st.session_state.analysis_complete = False
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Import views
from views import home, dashboard, progress, resources, immigration, contact, login

# AUTHENTICATION CHECK
if not st.session_state.authenticated:
    login.render()
    st.stop()  # Stop execution here, don't show the rest of the app

# Sidebar Navigation (Only visible if authenticated)
with st.sidebar:
    # Logout Button (Top of Sidebar)
    if st.button("🔒 Logout", key="logout_btn", use_container_width=True):
        st.session_state.authenticated = False
        st.session_state.analysis_complete = False
        st.rerun()
        
    # Profile Picture Logic
    # Profile Picture Logic
    if "profile_pic" not in st.session_state:
        st.session_state.profile_pic = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"

    col1, col2 = st.columns([1, 2])
    with col1:
         # Display current profile pic (as image or URL)
        if isinstance(st.session_state.profile_pic, str):
             st.image(st.session_state.profile_pic, width=60)
        else:
             st.image(st.session_state.profile_pic, width=60)
    
    with col2:
        st.title("DreamJob")

    # Upload Expander
    with st.expander("Edit Profile Photo"):
        uploaded_pic = st.file_uploader("Upload Image", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")
        if uploaded_pic is not None:
            image = Image.open(uploaded_pic)
            st.session_state.profile_pic = image
            st.rerun()

    # helper for programmatic navigation
    # Only force index if manually set by redirection logic
    default_index = 0
    selected_from_state = None
    
    if "manual_selection" in st.session_state and st.session_state.manual_selection:
        try:
             # Map string to index
            options_list = ["Home", "Dashboard", "Progress Matrix", "Learning Resources", "Immigration & Visa", "Contact Us"]
            default_index = options_list.index(st.session_state.manual_selection)
            selected_from_state = st.session_state.manual_selection
            st.session_state.manual_selection = None # Reset immediately
        except Exception:
            default_index = 0

    # Ensure consistent navigation state
    selected = option_menu(
        menu_title=None,
        options=["Home", "Dashboard", "Progress Matrix", "Learning Resources", "Immigration & Visa", "Contact Us"],
        icons=["house", "speedometer2", "list-task", "book", "globe", "envelope"],
        menu_icon="cast",
        default_index=default_index, 
        # key="main_nav", # Avoid key conflict for now, rely on reruns
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#4b6cb7", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "rgba(75, 108, 183, 0.1)"},
            "nav-link-selected": {"background-color": "#4b6cb7"},
        }
    )

    # If programmatic redirect happened, override local selection
    if selected_from_state:
        selected = selected_from_state
    
# Routing
if selected == "Home":
    home.render()
elif selected == "Dashboard":
    if st.session_state.analysis_complete:
        dashboard.render()
    else:
        st.warning("Please analyze your career path on the Home page first!")
        home.render()
elif selected == "Progress Matrix":
    progress.render()
elif selected == "Learning Resources":
    resources.render()
elif selected == "Immigration & Visa":
    immigration.render()
elif selected == "Contact Us":
    contact.render()
