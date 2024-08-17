import streamlit as st
from fpdf import FPDF
from PIL import Image
import os

def generate_pdf(data, profile_pic_path):
    pdf = FPDF()
    pdf.add_page()

    if profile_pic_path is not None:
        pic_width = 40
        pic_height = 40
        x_position = (210 - pic_width) / 2  
        pdf.image(profile_pic_path, x=x_position, y=10, w=pic_width, h=pic_height)
        pdf.set_xy(10, 60)  
    else:
        pdf.set_xy(10, 10)  

    # Add name
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(0, 10, txt=data["name"], ln=True, align='C')

    # Add contact information
    pdf.set_font("Arial", size=12)
    pdf.ln(5)
    pdf.cell(0, 10, txt=f"Email: {data['email']}", ln=True, align='C')
    pdf.cell(0, 10, txt=f"Phone: {data['phone']}", ln=True, align='C')
    pdf.cell(0, 10, txt=f"Address: {data['address']}", ln=True, align='C')

    pdf.ln(10)

    # Add the summary
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Summary", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, data["summary"])

    pdf.ln(10)

    # Add experience
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Experience", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for job in data["experience"]:
        pdf.cell(0, 10, txt=f"{job['title']} - {job['company']}", ln=True, align='L')
        pdf.cell(0, 10, txt=f"{job['start_date']} - {job['end_date']}", ln=True, align='L')
        pdf.multi_cell(0, 10, job["description"])
        pdf.ln(5)

    pdf.ln(10)

    # Add education
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(0, 10, txt="Education", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for edu in data["education"]:
        pdf.cell(0, 10, txt=f"{edu['degree']} - {edu['institution']}", ln=True, align='L')
        pdf.cell(0, 10, txt=f"{edu['graduation_year']}", ln=True, align='L')
        pdf.ln(5)

    return pdf.output(dest="S").encode("latin1")

# Streamlit App
st.title("Resume Builder")

# Form to capture user data
with st.form("resume_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email")
    phone = st.text_input("Phone Number")
    address = st.text_area("Address")
    summary = st.text_area("Summary")

    # Profile picture upload
    profile_pic = st.file_uploader("Upload Profile Picture", type=["jpg", "jpeg", "png"])
    
    # Experience section
    st.write("Experience")
    num_experience = st.number_input("Number of Jobs", min_value=1, step=1, value=1)
    experience = []
    for i in range(num_experience):
        st.subheader(f"Job {i+1}")
        title = st.text_input(f"Job Title {i+1}", key=f"title_{i}")
        company = st.text_input(f"Company {i+1}", key=f"company_{i}")
        start_date = st.text_input(f"Start Date {i+1}", key=f"start_date_{i}")
        end_date = st.text_input(f"End Date {i+1}", key=f"end_date_{i}")
        description = st.text_area(f"Description {i+1}", key=f"description_{i}")
        experience.append({
            "title": title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "description": description
        })

    # Education section
    st.write("Education")
    num_education = st.number_input("Number of Education Entries", min_value=1, step=1, value=1)
    education = []
    for i in range(num_education):
        st.subheader(f"Education {i+1}")
        degree = st.text_input(f"Degree {i+1}", key=f"degree_{i}")
        institution = st.text_input(f"Institution {i+1}", key=f"institution_{i}")
        graduation_year = st.text_input(f"Graduation Year {i+1}", key=f"graduation_year_{i}")
        education.append({
            "degree": degree,
            "institution": institution,
            "graduation_year": graduation_year
        })

    # Submit button
    submit = st.form_submit_button("Generate Resume")

if submit:
    data = {
        "name": name,
        "email": email,
        "phone": phone,
        "address": address,
        "summary": summary,
        "experience": experience,
        "education": education
    }

    if profile_pic is not None:
        profile_pic = Image.open(profile_pic)
        profile_pic = profile_pic.convert('RGB')
        profile_pic_path = "temp_profile_pic.jpg"
        profile_pic.save(profile_pic_path)
    else:
        profile_pic_path = None

    # Generate PDF
    pdf_data = generate_pdf(data, profile_pic_path)
    if profile_pic_path is not None and os.path.exists(profile_pic_path):
        os.remove(profile_pic_path)
    
     # Provide download link
    st.download_button("Download Resume", data=pdf_data, file_name="resume.pdf", mime="application/pdf")
