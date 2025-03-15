import os
import time
import base64
import json
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from email.message import EmailMessage
from pymongo import MongoClient
import ollama
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Load API Credentials
load_dotenv()
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_PATH")

if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

# MongoDB Connection
def get_student_details(email):
    client = MongoClient("mongodb+srv://sachdevarishav449:Parishu449%40@aplica.cozta.mongodb.net/")
    db = client["user-info"]
    collection = db["user-main-details"]
    student = collection.find_one({"email": email})
    return student

# Function to Generate Cold Email
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
- Use a **catchy email subject line** (Make it the **first line of output**).
- Start the email with **Hello,**.
- Highlight **why the company is great for applying for an internship**.
- Highlight **why the candidate is a great fit** for {company}.
- Make the email **longer and more detailed** (200-250 words).
- Ensure a **strong, professional closing**.
- End with **asking for a convenient time to connect**.
- Clearly state that the **resume is attached**.

Make sure the email ends with:
"Best regards,  
{student['full_name']}  
Email: {student['email']}  
Phone: {student['phone']}  
LinkedIn: {student['linkedin']}  

(Resume Attached)".
"""

    response = ollama.chat(model="llama2:7b", messages=[{"role": "user", "content": prompt}])
    email_text = response['message']['content']

    # Extract the first line as subject & remove it from email body
    email_lines = email_text.strip().split("\n", 1)
    subject_line = email_lines[0].replace("Subject:", "").strip() if len(email_lines) > 0 else "Internship Application"
    email_body = email_lines[1] if len(email_lines) > 1 else email_text

    return subject_line, email_body

# # Function to Authenticate Google
# def authenticate_google():
#     creds = None
#     token_file = "token.json"

#     if os.path.exists(token_file):
#         creds = Credentials.from_authorized_user_file(token_file)

#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file(
#             GOOGLE_CREDENTIALS,
#             scopes=["https://www.googleapis.com/auth/gmail.send"]
#         )
#         creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=False)
#         with open(token_file, "w") as token:
#             token.write(creds.to_json())

#     return creds
def authenticate_google():
    creds = None
    token_file = "token.json"

    # 🔹 If token.json exists, delete it to ensure a fresh authentication
    if os.path.exists(token_file):
        os.remove(token_file)  # ✅ Delete the existing token file

    flow = InstalledAppFlow.from_client_secrets_file(
        GOOGLE_CREDENTIALS,
        scopes=["https://www.googleapis.com/auth/gmail.send"]
    )

    creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=False)

    # Save new credentials for future use
    with open(token_file, "w") as token:
        token.write(creds.to_json())

    return creds



def send_email(to_email, subject, body, creds, attachment_path=None):
    url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"

    message = EmailMessage()
    message["To"] = to_email
    message["From"] = "me"
    message["Subject"] = subject
    message.set_content(body)

    # Attach file if provided
    if attachment_path:
        try:
            with open(attachment_path, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(attachment_path)
                message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
        except Exception as e:
            st.error(f"⚠️ Error attaching file: {e}")

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    payload = json.dumps({"raw": encoded_message})

    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"},
        data=payload,
    )

    return response.json()


# Streamlit UI
st.title("📩 AI-Powered Cold Email Generator & Bulk Sender")

# Section 1: Cold Email Generator
st.header("📧 Cold Email Generator")
email = st.text_input("Enter Your Registered Email:")
company = st.text_input("Enter Company Name:")
role = st.text_input("Enter Role:")

generated_subject = ""
generated_email_body = ""
# Ensure session state variables exist
if "subject" not in st.session_state or not st.session_state.subject:
    st.session_state.subject = ""
if "email_body" not in st.session_state or not st.session_state.email_body:
    st.session_state.email_body = ""

# Section 1: Cold Email Generator
if st.button("Generate Cold Email"):
    if not email or not company or not role:
        st.warning("⚠️ Please fill in all fields before generating the email.")
    else:
        student_details = get_student_details(email)
        if student_details:
            subject_line, email_body_text = generate_cold_email(student_details, company, role)
            
            # Only update session state if empty to avoid overwriting
            if not st.session_state.subject:
                st.session_state.subject = subject_line
            if not st.session_state.email_body:
                st.session_state.email_body = email_body_text
        else:
            st.error("❌ User not found in database!")

# Section 2: Bulk Email Sender
st.header("📤 Bulk Email Sender")

uploaded_file = st.file_uploader("Upload an Excel or CSV file with the emails column ", type=["xlsx", "csv"])

subject = st.text_input("Enter Email Subject", value=st.session_state.subject, key="email_subject")
email_body = st.text_area("Enter Email Body", value=st.session_state.email_body, height=350, key="email_body")
attachment_file = st.file_uploader("📎 Upload Attachment for Email (Optional)", type=["pdf", "docx", "png", "jpg", "txt"])

# Prevent clearing the autofilled email content when a file is uploaded
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    email_column = st.selectbox("Select the Email Column", df.columns)

    if st.button("Send Emails"):
        if subject.strip() and email_body.strip() and email_column:
            creds = authenticate_google()

            if creds:
                st.success("✅ Successfully authenticated! Sending emails...")
                # Save uploaded attachment temporarily
                attachment_path = None
                if attachment_file:
                    attachment_path = f"{attachment_file.name}"
                    with open(attachment_path, "wb") as f:
                        f.write(attachment_file.getbuffer())

                for email in df[email_column].dropna():
                    result = send_email(email, st.session_state.subject, st.session_state.email_body, creds, attachment_path)
                    st.write(f"📨 Email sent to {email}")
                
                if attachment_path:
                    os.remove(attachment_path)

                st.success("🎉 All emails sent successfully!")
            else:
                st.error("❌ Authentication failed. Please check your Google API credentials.")
        else:
            st.warning("⚠️ Please provide an email subject, body, and select the email column.")
            
st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
