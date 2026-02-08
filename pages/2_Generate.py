import streamlit as st
import streamlit.components.v1 as components
import base64
from utils import zip_html_file, generate_portfolio_html

st.set_page_config(page_title="Generate Portfolio", layout="centered")
st.title("🚀 Generate Portfolio Website")

if "user_data" not in st.session_state:
    st.warning("Please fill out your details first on the Create page.")
    st.stop()

data = st.session_state["user_data"]

photo_b64 = f"data:image/jpeg;base64,{base64.b64encode(data['photo']).decode()}" if data['photo'] else None
project_imgs_b64 = [f"data:image/jpeg;base64,{base64.b64encode(img).decode()}" for img in data['project_images']]
cert_imgs_b64 = [
    (f"data:application/pdf;base64,{base64.b64encode(cert).decode()}" if cert[:4] == b"%PDF"
     else f"data:image/jpeg;base64,{base64.b64encode(cert).decode()}")
    for cert in data['certificates']
]

projects_list = data['projects'].splitlines() if data['projects'].strip() else []
project_entries = "\n".join(projects_list)

prompt = f"""
You are a professional web designer.
Generate a complete responsive portfolio website in one HTML file using only inline CSS.

Include these sections in order:

1. Header
- Name: {data['name']}
- Role: {data['role']}

2. About
- Bio: {data['bio']}
- Email: {data['email']}

3. Skills
- {data['skills']}

{"4. Projects" + project_entries if project_entries else ""}

5. Contact section with email again.

Use responsive layout, sidebar layout, and visually neat formatting.
Only return valid HTML starting with <!DOCTYPE html> and ending with </html>. """

try:
    html = generate_portfolio_html(prompt)
except Exception:
    st.error("❌ Failed to generate portfolio using Gemini.")
    st.stop()

sidebar_html = "<div style='position:fixed; top:0; left:0; width:200px; height:100%; background:#f0f0f0; padding:20px; overflow:auto;'>"

if photo_b64:
    sidebar_html += f"<img src='{photo_b64}' width='100' style='border-radius:50%; display:block; margin:0 auto 20px;'>"

if cert_imgs_b64:
    sidebar_html += "<h4>Certificates</h4>"
    for cert in cert_imgs_b64:
        if "pdf" in cert:
            sidebar_html += f"<embed src='{cert}' width='200' height='175' type='application/pdf' style='margin-bottom:10px;'>"
        else:
            sidebar_html += f"<img src='{cert}' width='200' style='margin-bottom:10px;'>"

if project_imgs_b64:
    sidebar_html += "<h4>Projects</h4>"
    for img in project_imgs_b64:
        sidebar_html += f"<img src='{img}' width='200' height='175' style='margin-bottom:10px;'>"

sidebar_html += "</div>"

if "<body" in html and "</body>" in html:
    body_parts = html.split("<body", 1)
    tag_content, rest = body_parts[1].split(">", 1)
    html = body_parts[0] + f"<body{tag_content}>" + sidebar_html + f"<div style='margin-left:220px; padding:20px;'>" + rest.replace("</body>", "</div></body>")

st.session_state["final_html"] = html

if st.button("✨ Generate Portfolio Website"):
    st.success("Portfolio generated successfully!")

if "final_html" in st.session_state:
    st.subheader("🔍 Live Preview")
    components.html(st.session_state["final_html"], height=600, scrolling=True)

    zip_path = zip_html_file(st.session_state["final_html"])
    with open(zip_path, "rb") as f:
        st.download_button("📥 Download HTML ZIP", f, file_name="portfolio.zip")

if st.button("🔁 Generate Again"):
    del st.session_state["final_html"]
    st.rerun()
    
