import streamlit as st
import ollama
from pymongo import MongoClient

# Connect to MongoDB
def get_student_details(email):
    client = MongoClient("mongodb+srv://sachdevarishav449:Parishu449%40@aplica.cozta.mongodb.net/")
    db = client["user-info"]
    collection = db["user-main-details"]
    student = collection.find_one({"email": email})
    return student

# Function to Generate Cold Email Using Ollama
def generate_cold_email(student, company, role):
    prompt = f"""You are an expert in writing highly personalized, engaging, and professional cold emails.
Generate a compelling **cold email** for an internship at {company} as a {role}.
The email should be **tailored to {company}**, reflecting its industry, values, and mission.

**Candidate Details:**
- Name: {student['full_name']}
- Degree: {student['highest_degree']} in {student['field_of_study']} from {student['university']}
- Technical Skills: {', '.join(student['technical_skills'])}
- Internships: {', '.join(student['internships']) if student['internships'] else 'None'}

**Guidelines:**
- Use a **catchy email subject line**.
- Start the email with **Hello,**.
- Highlight **why the company is great for applying for an internship**.
- Highlight **why the candidate is a great fit** for {company}.
- Make the email **longer and more detailed** (200-250 words).
- Ensure a **strong, professional closing**.
- End the email with **asking for a convenient time to connect**.
- End with a **call to action**, asking for a conversation at HR's convenience.
- Clearly state that the **resume is attached**.
- The output should contain **only the email content**, with no extra formatting or explanations.

Make sure the email ends with:
"Best regards,  
{student['full_name']}  
Email: {student['email']}  
Phone: {student['phone']}  
LinkedIn: {student['linkedin']}  

(Resume Attached)".
"""

    response = ollama.chat(model="llama2", messages=[{"role": "user", "content": prompt}])
    
    email_text = response['message']['content']

    return email_text

# Streamlit UI
st.title("📩 AI-Powered Cold Email Generator")

# User Inputs
email = st.text_input("Enter Your Registered Email:")
company = st.text_input("Enter Company Name:")
role = st.text_input("Enter Role:")

# Generate Button
if st.button("Generate Cold Email"):
    if not email or not company or not role:
        st.warning("⚠️ Please fill in all fields before generating the email.")
    else:
        student_details = get_student_details(email)
        if student_details:
            cold_email = generate_cold_email(student_details, company, role)
            st.subheader("✅ Generated Cold Email:")
            st.write(cold_email)
        else:
            st.error("❌ User not found in database!")
