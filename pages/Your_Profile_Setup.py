# import streamlit as st
# from pymongo import MongoClient
# import os
# import urllib.parse
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()

# DB_NAME = os.getenv("DB")  
# C2=os.getenv("C2")

# username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
# password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

# MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# # MongoDB Connection
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# profiles_collection = db[C2]  

# # Redirect if not authenticated
# if "authenticated" not in st.session_state or not st.session_state.authenticated:
#     st.error("You must be logged in to access this page!")
#     st.stop()

# st.title(f"Welcome, {st.session_state.full_name}! Please complete your job application profile.")

# # --- Personal Details ---
# st.header("Personal Details")
# full_name = st.text_input("Full Name", st.session_state.full_name)
# email = st.text_input("Email", st.session_state.email, disabled=True)
# phone = st.text_input("Phone Number")
# address = st.text_input("Address")
# city = st.text_input("City")
# state = st.text_input("State")
# pincode = st.text_input("Pin Code")
# linkedin = st.text_input("LinkedIn Profile URL")
# github = st.text_input("GitHub Profile URL")
# portfolio = st.text_input("Portfolio Website (if any)")
# location = st.text_input("Current Location (City, Country)")

# # --- Education Details ---
# st.header("Education")
# highest_degree = st.selectbox("Highest Degree", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"])
# university = st.text_input("University/College Name")
# field_of_study = st.text_input("Field of Study (e.g., Computer Science, Electrical Engineering)")
# graduation_year = st.number_input("Year of Graduation", min_value=1900, max_value=2100, step=1)
# cgpa = st.number_input("CGPA (if applicable)", min_value=0.0, max_value=10.0, step=0.1)
# certifications = st.text_area("Certifications (Separate by commas)")

# # --- Work Experience ---
# st.header("Work Experience")
# has_experience = st.radio("Do you have prior work experience?", ["Yes", "No"])

# work_experience = []
# if has_experience == "Yes":
#     num_experiences = st.number_input("How many previous jobs have you had?", min_value=1, max_value=10, step=1)
#     for i in range(num_experiences):
#         with st.expander(f"Work Experience {i+1}"):
#             company_name = st.text_input(f"Company Name {i+1}")
#             job_title = st.text_input(f"Job Title {i+1}")
#             job_duration = st.text_input(f"Duration (e.g., Jan 2020 - Dec 2022) {i+1}")
#             job_responsibilities = st.text_area(f"Job Responsibilities {i+1}")
#             job_achievements = st.text_area(f"Key Achievements {i+1}")
#             work_experience.append({
#                 "company": company_name,
#                 "title": job_title,
#                 "duration": job_duration,
#                 "responsibilities": job_responsibilities,
#                 "achievements": job_achievements
#             })

# # --- Skills ---
# st.header("Skills")
# technical_skills = st.text_area("Technical Skills (e.g., Python, Java, SQL, React) (Separate by commas)")
# soft_skills = st.text_area("Soft Skills (e.g., Communication, Teamwork, Leadership) (Separate by commas)")

# # --- Projects ---
# st.header("Projects")
# num_projects = st.number_input("How many projects have you worked on?", min_value=0, max_value=10, step=1)
# projects = []
# for i in range(num_projects):
#     with st.expander(f"Project {i+1}"):
#         project_title = st.text_input(f"Project Title {i+1}")
#         project_description = st.text_area(f"Project Description {i+1}")
#         project_technologies = st.text_input(f"Technologies Used {i+1} (Separate by commas)")
#         project_github = st.text_input(f"GitHub/Portfolio Link {i+1}")
#         projects.append({
#             "title": project_title,
#             "description": project_description,
#             "technologies": project_technologies,
#             "github": project_github
#         })

# # --- Internships & Training ---
# st.header("Internships & Training")
# num_internships = st.number_input("How many internships or training programs have you completed?", min_value=0, max_value=10, step=1)
# internships = []
# for i in range(num_internships):
#     with st.expander(f"Internship/Training {i+1}"):
#         intern_company = st.text_input(f"Company/Institute Name {i+1}")
#         intern_role = st.text_input(f"Internship Role {i+1}")
#         intern_duration = st.text_input(f"Duration (e.g., 3 months) {i+1}")
#         intern_responsibilities = st.text_area(f"Key Learnings {i+1}")
#         internships.append({
#             "company": intern_company,
#             "role": intern_role,
#             "duration": intern_duration,
#             "responsibilities": intern_responsibilities
#         })

# # --- Career Preferences ---
# st.header("Career Preferences")
# remote_work = st.radio("Would you prefer remote work?", ["Yes", "No"])
# work_outside_india = st.radio("Would you consider working outside India?", ["Yes", "No", "Open to Both"])
# preferred_locations_india = st.text_area("Top 5 Preferred Locations in India (Separate by commas)", placeholder="e.g., Delhi, Mumbai, Hyderabad, Pune, Gurugram")
# #preferred_locations_abroad = st.text_area("Top 5 Preferred Locations Outside India (Separate by commas)")
# preferred_profiles = st.text_area("Top 3 Preferred Profiles (Separate by commas)", placeholder="e.g., Python Developer, Data Scientist")
# # Top 5 Preferred Locations (Outside India)
# if work_outside_india in ["Yes", "Open to Both"]:
#     preferred_locations_abroad = st.text_area(
#         "Top 5 Preferred Locations (Outside India) (Separate by commas)",
#         placeholder="e.g., New York, London, Sydney, Berlin, Toronto"
#     )
# else:
#     st.text_area(
#         "Top 5 Preferred Locations (Outside India) (Separate by commas)",
#         disabled=True,
#         value="N/A (Not applicable based on your preference)",
#         placeholder="N/A (Not applicable based on your preference)"
#     )
# # --- Resume Upload ---
# st.header("Upload Resume")
# resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# # --- Store User Profile Data in MongoDB ---
# def store_user_profile():
#     resume_data = resume.read() if resume is not None else None
#     profiles_collection.insert_one({
#         "email": email,
#         "full_name": full_name,
#         "phone": phone,
#         "linkedin": linkedin,
#         "github": github,
#         "portfolio": portfolio,
#         "location": location,
#         "highest_degree": highest_degree,
#         "university": university,
#         "field_of_study": field_of_study,
#         "graduation_year": graduation_year,
#         "cgpa": cgpa,
#         "certifications": certifications.split(","),
#         "work_experience": work_experience,
#         "technical_skills": technical_skills.split(","),
#         "soft_skills": soft_skills.split(","),
#         "projects": projects,
#         "internships": internships,
#         "resume": resume_data,
#         "career_preferences": {
#             "remote_work": remote_work,
#             "work_outside_india": work_outside_india,
#             "preferred_locations_india": preferred_locations_india.split(","),
#             "preferred_locations_abroad": preferred_locations_abroad.split(","),
#             "preferred_profiles": preferred_profiles.split(",")
#         }
#     })
#     return True

# if st.button("Save Profile"):
#     if resume:
#         store_user_profile()
#         st.success("Profile saved successfully!")
#         st.switch_page("pages/Your_Dashboard.py")  # Redirect to dashboard

#     else:
#         st.error("Please upload your resume.")

# st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))




import streamlit as st
from pymongo import MongoClient
import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DB_NAME = os.getenv("DB")  
C2 = os.getenv("C2")

username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))

MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# MongoDB Connection
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
profiles_collection = db[C2]

# Redirect if not authenticated
if "authenticated" not in st.session_state or not st.session_state.authenticated:
    st.error("You must be logged in to access this page!")
    st.stop()

st.title(f"Welcome, {st.session_state.full_name}! Update Your Job Application Profile.")

# Fetch existing profile from MongoDB
existing_profile = profiles_collection.find_one({"email": st.session_state.email})

# Helper function to pre-fill data or use default values
def get_value(field, default=""):
    return existing_profile.get(field, default) if existing_profile else default

# --- Personal Details ---
st.header("Personal Details")
full_name = st.text_input("Full Name", get_value("full_name", st.session_state.full_name))
email = st.text_input("Email", st.session_state.email, disabled=True)
phone = st.text_input("Phone Number", get_value("phone"))
address = st.text_input("Address", get_value("address"))
city = st.text_input("City", get_value("city"))
state = st.text_input("State", get_value("state"))
pincode = st.text_input("Pin Code", get_value("pincode"))
linkedin = st.text_input("LinkedIn Profile URL", get_value("linkedin"))
github = st.text_input("GitHub Profile URL", get_value("github"))
portfolio = st.text_input("Portfolio Website (if any)", get_value("portfolio"))
location = st.text_input("Current Location (City, Country)", get_value("location"))

# --- Education Details ---
st.header("Education")
highest_degree = st.selectbox("Highest Degree", ["High School", "Diploma", "Bachelor's", "Master's", "PhD"], index=["High School", "Diploma", "Bachelor's", "Master's", "PhD"].index(get_value("highest_degree", "Bachelor's")))
university = st.text_input("University/College Name", get_value("university"))
course = st.text_input("Course", get_value("course"))
field_of_study = st.text_input("Field of Study", get_value("field_of_study"))
graduation_year = st.number_input("Year of Graduation", min_value=1900, max_value=2100, step=1, value=int(get_value("graduation_year", 2025)))
cgpa = st.number_input("CGPA (if applicable)", min_value=0.0, max_value=10.0, step=0.1, value=float(get_value("cgpa", 0.0)))
certifications = st.text_area("Certifications (Separate by commas)", ",".join(get_value("certifications", [])))

# # --- Work Experience ---
# st.header("Work Experience")
# has_experience = st.radio("Do you have prior work experience?", ["Yes", "No"], index=0 if get_value("work_experience") else 1)

# work_experience = []
# if has_experience == "Yes":
#     # Get existing work experience count or default to 1
#     existing_experiences = get_value("work_experience", [])
#     num_experiences = st.number_input(
#         "How many previous jobs have you had?", 
#         min_value=1, max_value=10, step=1, 
#         value=len(existing_experiences) if existing_experiences else 1
#     )

#     for i in range(num_experiences):
#         exp = existing_experiences[i] if i < len(existing_experiences) else {}  # Pre-fill if exists
#         with st.expander(f"Work Experience {i+1}"):
#             company_name = st.text_input(f"Company Name {i+1}", exp.get("company", ""))
#             job_title = st.text_input(f"Job Title {i+1}", exp.get("title", ""))
#             job_duration = st.text_input(f"Duration (e.g., Jan 2020 - Dec 2022) {i+1}", exp.get("duration", ""))
#             job_responsibilities = st.text_area(f"Job Responsibilities {i+1}", exp.get("responsibilities", ""))
#             job_achievements = st.text_area(f"Key Achievements {i+1}", exp.get("achievements", ""))
            
#             work_experience.append({
#                 "company": company_name,
#                 "title": job_title,
#                 "duration": job_duration,
#                 "responsibilities": job_responsibilities,
#                 "achievements": job_achievements
#             })
# else:
#     work_experience = []  # If "No", clear the work experience list

# --- Skills ---
st.header("Skills")
technical_skills = st.text_area("Technical Skills (Separate by commas)", ",".join(get_value("technical_skills", [])))
soft_skills = st.text_area("Soft Skills (Separate by commas)", ",".join(get_value("soft_skills", [])))

# --- Projects ---
st.header("Projects")
existing_projects = get_value("projects", [])
new_projects = []

# Get existing project count or default to 1
num_projects = st.number_input(
    "How many projects have you worked on?",
    min_value=0, max_value=10, step=1,
    value=len(existing_projects) if existing_projects else 1
)

for i in range(num_projects):
    proj = existing_projects[i] if i < len(existing_projects) else {}  # Pre-fill if exists
    with st.expander(f"Project {i+1}"):
        project_title = st.text_input(f"Project Title {i+1}", proj.get("title", ""))
        project_description = st.text_area(f"Project Description {i+1}", proj.get("description", ""))
        project_technologies = st.text_input(f"Technologies Used {i+1} (Separate by commas)", proj.get("technologies", ""))
        project_github = st.text_input(f"GitHub/Portfolio Link {i+1}", proj.get("github", ""))

        new_projects.append({
            "title": project_title,
            "description": project_description,
            "technologies": project_technologies,
            "github": project_github
        })

# --- Internships & Training ---
st.header("Internships & Training")
existing_internships = get_value("internships", [])
new_internships = []

# Get existing count or default to 1
num_internships = st.number_input(
    "How many internships or training programs have you completed?",
    min_value=0, max_value=10, step=1,
    value=len(existing_internships) if existing_internships else 1
)

for i in range(num_internships):
    intern = existing_internships[i] if i < len(existing_internships) else {}  # Pre-fill if exists
    with st.expander(f"Internship/Training {i+1}"):
        intern_company = st.text_input(f"Company/Institute Name {i+1}", intern.get("company", ""))
        intern_role = st.text_input(f"Internship Role {i+1}", intern.get("role", ""))
        intern_duration = st.text_input(f"Duration (e.g., 3 months) {i+1}", intern.get("duration", ""))
        intern_responsibilities = st.text_area(f"Key Learnings {i+1}", intern.get("responsibilities", ""))

        new_internships.append({
            "company": intern_company,
            "role": intern_role,
            "duration": intern_duration,
            "responsibilities": intern_responsibilities
        })

# --- Career Preferences ---
st.header("Career Preferences")

remote_work = st.radio(
    "Would you prefer remote work?",
    ["Yes", "No"],
    index=["Yes", "No"].index(get_value("career_preferences.remote_work", "Yes"))
)

work_outside_india = st.radio(
    "Would you consider working outside India?",
    ["Yes", "No", "Open to Both"],
    index=["Yes", "No", "Open to Both"].index(get_value("career_preferences.work_outside_india", "Open to Both"))
)

preferred_locations_india = st.text_area(
    "Top 5 Preferred Locations in India (Separate by commas)",
    placeholder="e.g., Delhi, Mumbai, Hyderabad, Pune, Gurugram",  # Placeholder text
    value=", ".join(get_value("career_preferences.preferred_locations_india", []))  # Only fill if data exists
)

preferred_profiles = st.text_area(
    "Top 3 Preferred Profiles (Separate by commas)",
    placeholder="e.g., Python Developer, Data Scientist",  # Placeholder text
    value=", ".join(get_value("career_preferences.preferred_profiles", []))  # Only fill if data exists
)

if work_outside_india in ["Yes", "Open to Both"]:
    preferred_locations_abroad = st.text_area(
        "Top 5 Preferred Locations (Outside India) (Separate by commas)",
        placeholder="e.g., New York, London, Sydney, Berlin, Toronto",  # Placeholder text
        value=", ".join(get_value("career_preferences.preferred_locations_abroad", []))  # Only fill if data exists
    )
else:
    st.text_area(
        "Top 5 Preferred Locations (Outside India) (Separate by commas)",
        disabled=True,
        value="N/A (Not applicable based on your preference)",
        placeholder="N/A (Not applicable based on your preference)"
    )


# --- Resume Upload ---
st.header("Upload Resume")
resume = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# --- Store or Update User Profile in MongoDB ---
def store_or_update_profile():
    resume_data = resume.read() if resume is not None else get_value("resume", None)
    profile_data = {
        "email": email,
        "full_name": full_name,
        "phone": phone,
        "address": address,
        "city": city,
        "state": state,
        "pincode": pincode,
        "linkedin": linkedin,
        "github": github,
        "portfolio": portfolio,
        "location": location,
        "highest_degree": highest_degree,
        "university": university,
        "course": course,
        "internships": new_internships,
        "field_of_study": field_of_study,
        "graduation_year": graduation_year,
        "cgpa": cgpa,
        "certifications": certifications.split(",") if certifications else [],
        "technical_skills": technical_skills.split(",") if technical_skills else [],
        "soft_skills": soft_skills.split(",") if soft_skills else [],
        "projects": new_projects,
        "resume": resume_data,
        "career_preferences": {
            "remote_work": remote_work,
            "work_outside_india": work_outside_india,
            "preferred_locations_india": preferred_locations_india.split(",") if preferred_locations_india else [],
            "preferred_locations_abroad": preferred_locations_abroad.split(",") if preferred_locations_abroad else [],
            "preferred_profiles": preferred_profiles.split(",") if preferred_profiles else []
        }
    }

    # Update existing profile or insert new
    profiles_collection.update_one({"email": email}, {"$set": profile_data}, upsert=True)

if st.button("Save Profile"):
    store_or_update_profile()
    st.success("Profile updated successfully!")
    st.switch_page("pages/Your_Dashboard.py")  # Redirect to dashboard

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
