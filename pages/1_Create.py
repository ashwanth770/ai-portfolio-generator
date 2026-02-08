import streamlit as st

st.set_page_config(page_title="Create Portfolio", layout="centered")
st.title("📝 Enter Your Portfolio Info")

with st.form("portfolio_form"):
    name = st.text_input("Your Full Name")
    email = st.text_input("Email Address")
    role = st.text_input("Your Role / Title", placeholder="e.g. Data Scientist")
    bio = st.text_area("Short Bio")
    skills = st.text_input("Skills (comma-separated)", placeholder="Python, Machine Learning, SQL")
    projects = st.text_area("Projects (one per line: title - description - link)", height=150)
    project_images = st.file_uploader("Upload Project Images (optional)", type=["jpg", "png", "jpeg"], accept_multiple_files=True)
    certificates = st.file_uploader("Upload Certificates (optional)", type=["pdf", "jpg", "png"], accept_multiple_files=True)
    photo = st.file_uploader("Upload Profile Photo", type=["jpg", "png", "jpeg"])

    submitted = st.form_submit_button("Save Info")
    if submitted:
        st.session_state["user_data"] = {
            "name": name,
            "email": email,
            "role": role,
            "bio": bio,
            "skills": skills,
            "projects": projects,
            "project_images": [f.read() for f in project_images] if project_images else [],
            "certificates": [f.read() for f in certificates] if certificates else [],
            "photo": photo.read() if photo else None,
            "photo_name": photo.name if photo else None
        }
        st.success("Saved! Now go to 'Generate Portfolio' from sidebar.")
        
