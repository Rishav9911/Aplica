import streamlit as st
from pymongo import MongoClient
import ollama
from datetime import date
import urllib.parse
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os

load_dotenv()

# Connect to MongoDB
def get_student_details(email):
    # MongoDB connection details
    username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
    password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

    MONGO_URI = "mongodb+srv://{}:{}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority".format(username, password)

    # MongoDB Connection
    client = MongoClient(MONGO_URI)
    db = client["user-info"] 
    collection = db["user-main-details"] 

    return collection.find_one({"email": email})

# Generate Cover Letter
def generate_cover_letter(email, company, job_title, job_description):
    student = get_student_details(email)
    if not student:
        return "User not found in the database!"

    today_date = date.today().strftime('%B %d, %Y')

    # Prompt for Ollama
    
    prompt = f"""
    You are an expert in writing highly professional, structured, and engaging cover letters.
    Generate a well-formatted cover letter for {student['full_name']} applying for the {job_title} position at {company}.

    Candidate Details:
    - Name: {student['full_name']}
    - University: {student['university']}
    - Degree: {student['highest_degree']} in {student['field_of_study']}
    - Technical Skills: {', '.join(student['technical_skills'])}
    - Internship/Project Experience: {', '.join(student['internships']) if student['internships'] else 'None'}
    - LinkedIn: {student['linkedin']}
    - Contact Email: {student['email']}
    - Contact Phone: {student['phone']}
    
    Job Description:
    {job_description}

    Formatting Guidelines:
    1. **Header** (Include candidate's details & today's date: {today_date}).
    2. **Salutation** (Use "Dear [Hiring Manager's Name]," or "Dear Hiring Manager,").
    3. **Opening Paragraph**: Excitement about {company}, connection to its mission, values, or innovations.
    4. **Body Paragraph**: Relevant skills, projects, and internships linked to {company} and connect past experience to the job role at {company}.
    5. **Closing Paragraph**: Reiterate interest, request an interview, mention resume attachment.
    6. **Sign-off**: "Best regards," followed by candidate’s name and contact info.
    7. Only print the content of each heading, not the heading names itself.

    Writing Style:
    1. Keep it concise and professional (Max 300-350 words).
    2. Avoid placeholders like [University Name], [Degree Name], etc.
    3. Ensure smooth, natural flow between paragraphs.
    4. Avoid excessive enthusiasm—keep the tone confident, clear, and engaging.

    """

    # Call Ollama model
    response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])
    cover_letter = response["message"]["content"]

    # Append Contact Details
    if "Best regards," not in cover_letter:
        cover_letter += f"\n\nBest regards,\n{student['full_name']}\nEmail: {student['email']}\nPhone: {student['phone']}\nLinkedIn: {student['linkedin']}\n(Resume Attached)"

    return cover_letter


# 🚀 Streamlit UI
st.title("📄 AI Cover Letter Generator")
st.write("Generate a professional cover letter tailored to your details and job description.")

email = st.text_input("Enter your email:")
company = st.text_input("Company Name:")
job_title = st.text_input("Job Title:")
job_description = st.text_area("Job Description:", height=150)

if st.button("Generate Cover Letter"):
    if email and company and job_title and job_description:
        with st.spinner("Generating your cover letter..."):
            cover_letter = generate_cover_letter(email, company, job_title, job_description)
        st.success("✅ Cover Letter Generated!")
        st.text_area("Your Cover Letter:", cover_letter, height=300)
    else:
        st.error("⚠️ Please fill all fields!")

