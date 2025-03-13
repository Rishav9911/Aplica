import os
import time
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import base64
import json
import requests
from email.message import EmailMessage

# Load API Credentials from .env file
load_dotenv()
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS_PATH")

def authenticate_google():
    creds = None
    token_file = "token.json"

    # Load existing credentials if available
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            GOOGLE_CREDENTIALS,
            scopes=["https://www.googleapis.com/auth/gmail.send"]
        )

        # Change port to avoid conflict with Streamlit's default port
        creds = flow.run_local_server(port=8080, redirect_uri_trailing_slash=False)

        # Save credentials for future use
        with open(token_file, "w") as token:
            token.write(creds.to_json())

    return creds



# Function to send email using Gmail API
def send_email(to_email, subject, body, creds):
    """
    Send an email using Gmail API.
    """
    url = "https://www.googleapis.com/gmail/v1/users/me/messages/send"
    
    # Email format
    message = EmailMessage()
    message["To"] = to_email
    message["From"] = "me"  # Authenticated user
    message["Subject"] = subject
    message.set_content(body)

    # Encode message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    payload = json.dumps({"raw": encoded_message})

    # Send email via Gmail API
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {creds.token}", "Content-Type": "application/json"},
        data=payload,
    )

    return response.json()

# Streamlit UI
st.title("📧 Bulk Email Sender (Like Mergo)")

uploaded_file = st.file_uploader("Upload an Excel or CSV file", type=["xlsx", "csv"])
subject = st.text_input("Enter Email Subject")
email_body = st.text_area("Enter Email Body")

if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    email_column = st.selectbox("Select the Email Column", df.columns)

    if st.button("Send Emails"):
        if subject and email_body and email_column:
            st.write("🔄 **Authenticating with Google API...**")
            creds = authenticate_google()
            
            if creds:
                st.success("✅ Successfully authenticated! Sending emails...")

                for email in df[email_column].dropna():
                    result = send_email(email, subject, email_body, creds)
                    st.write(f"📨 Email sent to {email}: {result}")

                st.success("🎉 All emails sent successfully!")
            else:
                st.error("❌ Authentication failed. Please check your Google API credentials.")
        else:
            st.warning("⚠️ Please provide an email subject, body, and select the email column.")
