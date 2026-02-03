import streamlit as st

def render():
    st.title("Contact Us")
    st.markdown("We'd love to hear from you! If you have any questions, feedback, or need support, please get in touch.")
    
    st.info("📧 **Email:** tanishtha46@gmail.com")
    
    st.markdown("---")
    
    st.subheader("Send us a message directly")
    
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        subject = st.text_input("Subject")
        message = st.text_area("Message")
        
        submit_button = st.form_submit_button("Create Email Draft")
        
        if submit_button:
            if not name or not subject or not message:
                st.error("Please fill out all fields.")
            else:
                # Create mailto link
                subject_safe = subject.replace(" ", "%20")
                body_safe = f"Hi, my name is {name}.\n\n{message}".replace("\n", "%0D%0A").replace(" ", "%20")
                mailto_link = f"mailto:tanishtha46@gmail.com?subject={subject_safe}&body={body_safe}"
                
                st.markdown(f"""
                    <a href="{mailto_link}" target="_blank" style="text-decoration: none;">
                        <button style="
                            background-color: #4CAF50; 
                            border: none; 
                            color: white; 
                            padding: 15px 32px; 
                            text-align: center; 
                            text-decoration: none; 
                            display: inline-block; 
                            font-size: 16px; 
                            margin: 4px 2px; 
                            cursor: pointer; 
                            border-radius: 4px;">
                            🚀 Open Email App
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                st.info("Note: If the button above doesn't open your email app, please copy the message and send it manually to: **tanishtha46@gmail.com**")
