# import os
# import requests
# import random
# import torch
# import torch.nn.functional as F
# import pandas as pd
# import streamlit as st
# import urllib.parse
# import time
# from bs4 import BeautifulSoup
# from sentence_transformers import SentenceTransformer
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from io import BytesIO

# # Load environment variables
# load_dotenv()

# # MongoDB Setup
# DB_NAME = os.getenv("DB")
# C2 = os.getenv("C2")
# username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
# password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
# MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# # Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# profiles_collection = db[C2]

# # Scraper API Key
# API_KEY = os.getenv("SCRAPER_API_KEY")

# # Load locally saved model
# MODEL_PATH = "local_model"
# model = SentenceTransformer(MODEL_PATH)

# # User-Agent rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
# ]

# def get_indeed_url(location):
#     """Returns the correct Indeed domain based on location."""
#     if "India" in location:
#         return "https://in.indeed.com/jobs"
#     elif "UK" in location or "London" in location:
#         return "https://uk.indeed.com/jobs"
#     elif "Canada" in location or "Toronto" in location:
#         return "https://ca.indeed.com/jobs"
#     else:
#         return "https://www.indeed.com/jobs"

# def fetch_user_preferences():
#     """Fetches the user's job profiles, locations, and resume from MongoDB."""
#     if "email" not in st.session_state:
#         st.error("User not authenticated.")
#         st.stop()

#     user_profile = profiles_collection.find_one({"email": st.session_state.email})
#     if user_profile:
#         job_titles = user_profile.get("career_preferences", {}).get("preferred_profiles", [])
#         locations_india = user_profile.get("career_preferences", {}).get("preferred_locations_india", [])
#         locations_abroad = user_profile.get("career_preferences", {}).get("preferred_locations_abroad", [])
#         preferred_locations = locations_india + locations_abroad

#         # Fetch resume
#         resume_data = user_profile.get("resume")
#         resume_text = extract_text_from_resume(resume_data) if resume_data else None

#         return job_titles, preferred_locations, resume_text
#     return [], [], None

# def extract_text_from_resume(binary_resume):
#     """Extracts text from a resume stored in MongoDB (Binary format)."""
#     try:
#         pdf_reader = PdfReader(BytesIO(binary_resume))
#         text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
#         return text
#     except Exception as e:
#         st.warning(f"Error extracting text from resume: {e}")
#         return None

# def get_job_description(job_url):
#     """Fetches the full job description from the job's detail page."""
#     headers = {"User-Agent": random.choice(USER_AGENTS)}
#     proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={job_url}"

#     try:
#         response = requests.get(proxy_url, headers=headers)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             description_tag = soup.find("div", id="jobDescriptionText")
#             return description_tag.get_text("\n", strip=True) if description_tag else "N/A"
#     except Exception as e:
#         st.warning(f"Error fetching job description: {e}")

#     return "N/A"

# def scrape_indeed(job_title, location, num_pages=2):
#     """Scrapes Indeed job listings for a given title and location."""
#     base_url = get_indeed_url(location)
#     job_list = []

#     for page in range(0, num_pages * 10, 10):
#         url = f"{base_url}?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&sr=directhire&start={page}"
#         proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={url}"
#         headers = {"User-Agent": random.choice(USER_AGENTS)}

#         try:
#             response = requests.get(proxy_url, headers=headers)
#             if response.status_code != 200:
#                 st.warning(f"Error {response.status_code} - Could not fetch {url}")
#                 continue
#         except Exception as e:
#             st.warning(f"Exception during request: {e}")
#             continue

#         soup = BeautifulSoup(response.text, "html.parser")
#         job_cards = soup.select("div.job_seen_beacon")

#         for job in job_cards:
#             title = job.select_one("h2.jobTitle a")
#             title = title.get_text(strip=True) if title else "N/A"

#             company = job.select_one("span.companyName")
#             company = company.get_text(strip=True) if company else "N/A"

#             location_tag = job.select_one("div.companyLocation")
#             location = location_tag.get_text(strip=True) if location_tag else "N/A"

#             job_url = job.select_one("h2.jobTitle a")
#             job_url = "https://in.indeed.com" + job_url["href"] if job_url else "N/A"

#             job_description = get_job_description(job_url) if job_url != "N/A" else "N/A"

#             job_list.append({
#                 "Title": title,
#                 "Company": company,
#                 "Location": location,
#                 "Job URL": job_url,
#                 "Full Description": job_description
#             })

#         time.sleep(random.randint(2, 5))

#     return job_list

# def match_jobs_with_resume(resume_text, jobs, threshold=0.4):
#     """Matches resume with job descriptions using AI-based similarity."""
#     resume_embedding = model.encode(resume_text, convert_to_tensor=True).view(1, -1)

#     matched_jobs = []
#     for job in jobs:
#         job_description = job["Full Description"]
#         if job_description == "N/A" or len(job_description) < 50:
#             continue

#         job_embedding = model.encode(job_description, convert_to_tensor=True).view(1, -1)
#         similarity = F.cosine_similarity(resume_embedding, job_embedding, dim=1).item()

#         if similarity >= threshold:
#             job["Similarity Score"] = round(similarity, 2)
#             matched_jobs.append(job)

#     return sorted(matched_jobs, key=lambda x: x["Similarity Score"], reverse=True)

# # Streamlit UI
# st.title("🎯 AI-Powered Job Finder")

# job_profiles, job_locations, resume_text = fetch_user_preferences()

# st.subheader("📌 Select or Enter a Job Profile")
# selected_job = st.selectbox("Choose a Job Profile:", job_profiles)
# custom_job = st.text_input("Or Enter a Custom Job Profile:")

# st.subheader("🌍 Select a Location")
# selected_location = st.selectbox("Choose a Location:", job_locations)

# view_option = st.radio(
#     "Choose how you want to view the jobs:",
#     ("View All Jobs", "View Only Top 5 Matches")
# )

# if st.button("🔎 Find Jobs"):
#     if not resume_text:
#         st.error("No resume found in your profile. Please upload a resume in your profile settings.")
#     else:
#         jobs = scrape_indeed(custom_job if custom_job else selected_job, selected_location)
#         matched_jobs = match_jobs_with_resume(resume_text, jobs)

#         if matched_jobs:
#             st.success(f"✅ Found {len(matched_jobs)} relevant jobs!")
#             if view_option == "View Only Top 5 Matches":
#                 matched_jobs = matched_jobs[:5]  # Show only top 5 jobs

#             df = pd.DataFrame(matched_jobs)
#             st.dataframe(df)
#         else:
#             st.warning("No highly relevant jobs found based on AI matching.")

# st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))


# import os
# import requests
# import random
# import torch
# import torch.nn.functional as F
# import pandas as pd
# import streamlit as st
# import urllib.parse
# import time
# from bs4 import BeautifulSoup
# from sentence_transformers import SentenceTransformer
# from pymongo import MongoClient
# from dotenv import load_dotenv
# from PyPDF2 import PdfReader
# from io import BytesIO

# # Load environment variables
# load_dotenv()

# # MongoDB Setup
# DB_NAME = os.getenv("DB")
# C2 = os.getenv("C2")
# username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
# password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
# MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# # Connect to MongoDB
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# profiles_collection = db[C2]

# # Scraper API Key
# API_KEY = os.getenv("SCRAPER_API_KEY")

# # Load locally saved model
# MODEL_PATH = "local_model"
# model = SentenceTransformer(MODEL_PATH)

# # User-Agent rotation
# USER_AGENTS = [
#     "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
#     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
#     "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
# ]

# def get_indeed_url(location):
#     """Returns the correct Indeed domain based on location."""
#     if "India" in location:
#         return "https://in.indeed.com/jobs"
#     elif "UK" in location or "London" in location:
#         return "https://uk.indeed.com/jobs"
#     elif "Canada" in location or "Toronto" in location:
#         return "https://ca.indeed.com/jobs"
#     else:
#         return "https://www.indeed.com/jobs"

# def fetch_user_preferences():
#     """Fetches the user's job profiles, locations, and resume from MongoDB."""
#     if "email" not in st.session_state:
#         st.error("User not authenticated.")
#         st.stop()

#     user_profile = profiles_collection.find_one({"email": st.session_state.email})
#     if user_profile:
#         job_titles = user_profile.get("career_preferences", {}).get("preferred_profiles", [])
#         locations_india = user_profile.get("career_preferences", {}).get("preferred_locations_india", [])
#         locations_abroad = user_profile.get("career_preferences", {}).get("preferred_locations_abroad", [])
#         preferred_locations = locations_india + locations_abroad

#         # Fetch resume
#         resume_data = user_profile.get("resume")
#         resume_text = extract_text_from_resume(resume_data) if resume_data else None

#         return job_titles, preferred_locations, resume_text
#     return [], [], None

# def extract_text_from_resume(binary_resume):
#     """Extracts text from a resume stored in MongoDB (Binary format)."""
#     try:
#         pdf_reader = PdfReader(BytesIO(binary_resume))
#         text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
#         return text
#     except Exception as e:
#         st.warning(f"Error extracting text from resume: {e}")
#         return None

# def get_job_description(job_url):
#     """Fetches the full job description from the job's detail page."""
#     headers = {"User-Agent": random.choice(USER_AGENTS)}
#     proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={job_url}"

#     try:
#         response = requests.get(proxy_url, headers=headers)
#         if response.status_code == 200:
#             soup = BeautifulSoup(response.text, "html.parser")
#             description_tag = soup.find("div", id="jobDescriptionText")
#             return description_tag.get_text("\n", strip=True) if description_tag else "N/A"
#     except Exception as e:
#         st.warning(f"Error fetching job description: {e}")

#     return "N/A"

# def scrape_indeed(job_title, location, num_pages=2):
#     """Scrapes Indeed job listings for a given title and location."""
#     base_url = get_indeed_url(location)
#     job_list = []

#     for page in range(0, num_pages * 10, 10):
#         url = f"{base_url}?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&sr=directhire&start={page}"
#         proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={url}"
#         headers = {"User-Agent": random.choice(USER_AGENTS)}

#         try:
#             response = requests.get(proxy_url, headers=headers)
#             if response.status_code != 200:
#                 st.warning(f"Error {response.status_code} - Could not fetch {url}")
#                 continue
#         except Exception as e:
#             st.warning(f"Exception during request: {e}")
#             continue

#         soup = BeautifulSoup(response.text, "html.parser")
#         job_cards = soup.select("div.job_seen_beacon")

#         for job in job_cards:
#             title = job.select_one("h2.jobTitle a")
#             title = title.get_text(strip=True) if title else "N/A"

#             company = job.select_one("span.companyName")
#             company = company.get_text(strip=True) if company else "N/A"

#             location_tag = job.select_one("div.companyLocation")
#             location = location_tag.get_text(strip=True) if location_tag else "N/A"

#             job_url = job.select_one("h2.jobTitle a")
#             job_url = "https://in.indeed.com" + job_url["href"] if job_url else "N/A"

#             job_description = get_job_description(job_url) if job_url != "N/A" else "N/A"

#             job_list.append({
#                 "Title": title,
#                 "Company": company,
#                 "Location": location,
#                 "Job URL": job_url,
#                 "Full Description": job_description
#             })

#         time.sleep(random.randint(2, 5))

#     return job_list

# def match_jobs_with_resume(resume_text, jobs, threshold=0.4):
#     """Matches resume with job descriptions using AI-based similarity."""
#     resume_embedding = model.encode(resume_text, convert_to_tensor=True).view(1, -1)

#     matched_jobs = []
#     for job in jobs:
#         job_description = job["Full Description"]
#         if job_description == "N/A" or len(job_description) < 50:
#             continue

#         job_embedding = model.encode(job_description, convert_to_tensor=True).view(1, -1)
#         similarity = F.cosine_similarity(resume_embedding, job_embedding, dim=1).item()

#         if similarity >= threshold:
#             job["Similarity Score"] = round(similarity, 2)
#             matched_jobs.append(job)

#     return sorted(matched_jobs, key=lambda x: x["Similarity Score"], reverse=True)

# # Streamlit UI
# st.title("🎯 AI-Powered Job Finder")

# job_profiles, job_locations, resume_text = fetch_user_preferences()

# st.subheader("📌 Select or Enter a Job Profile")
# selected_job = st.selectbox("Choose a Job Profile:", job_profiles)
# custom_job = st.text_input("Or Enter a Custom Job Profile:")

# st.subheader("🌍 Select a Location")
# selected_location = st.selectbox("Choose a Location:", job_locations)

# view_option = st.radio(
#     "Choose how you want to view the jobs:",
#     ("View All Jobs", "View Only Top 5 Matches")
# )

# if st.button("🔎 Find Jobs"):
#     if not resume_text:
#         st.error("No resume found in your profile. Please upload a resume in your profile settings.")
#     else:
#         jobs = scrape_indeed(custom_job if custom_job else selected_job, selected_location)
#         matched_jobs = match_jobs_with_resume(resume_text, jobs)

#         if matched_jobs:
#             st.success(f"✅ Found {len(matched_jobs)} relevant jobs!")
#             if view_option == "View Only Top 5 Matches":
#                 matched_jobs = matched_jobs[:5]

#             for job in matched_jobs:
#                 st.markdown(f"### **{job['Title']}** at {job['Company']} ({job['Location']})")
#                 st.markdown(f"[🔗 Apply Now]({job['Job URL']})  \n🔥 **Match Score:** {job['Similarity Score']:.2f}")
#                 with st.expander("📄 **Job Description**"):
#                     st.write(job["Full Description"])
#                 st.write("---")
#         else:
#             st.warning("No highly relevant jobs found based on AI matching.")

# st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))

# #TRY THIS AGAIN
import os
import requests
import random
import torch
import torch.nn.functional as F
import pandas as pd
import streamlit as st
import urllib.parse
import time
from bs4 import BeautifulSoup
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from io import BytesIO

# Load environment variables
load_dotenv()

# MongoDB Setup
DB_NAME = os.getenv("DB")
C2 = os.getenv("C2")
username = urllib.parse.quote_plus(os.getenv("MONGO_USERNAME"))
password = urllib.parse.quote_plus(os.getenv("MONGO_PASSWORD"))
MONGO_URI = f"mongodb+srv://{username}:{password}@aplica.cozta.mongodb.net/?retryWrites=true&w=majority"

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
profiles_collection = db[C2]

# Scraper API Key
API_KEY = os.getenv("SCRAPER_API_KEY")

# Load locally saved model
MODEL_PATH = "local_model"
model = SentenceTransformer(MODEL_PATH)

# User-Agent rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

def get_indeed_url(location):
    """Returns the correct Indeed domain based on location."""
    if "India" in location:
        return "https://in.indeed.com/jobs"
    elif "UK" in location or "London" in location:
        return "https://uk.indeed.com/jobs"
    elif "Canada" in location or "Toronto" in location:
        return "https://ca.indeed.com/jobs"
    else:
        return "https://www.indeed.com/jobs"

def fetch_user_preferences():
    """Fetches the user's job profiles, locations, and resume from MongoDB."""
    if "email" not in st.session_state:
        st.error("User not authenticated.")
        st.stop()

    user_profile = profiles_collection.find_one({"email": st.session_state.email})
    if user_profile:
        job_titles = user_profile.get("career_preferences", {}).get("preferred_profiles", [])
        locations_india = user_profile.get("career_preferences", {}).get("preferred_locations_india", [])
        locations_abroad = user_profile.get("career_preferences", {}).get("preferred_locations_abroad", [])
        preferred_locations = locations_india + locations_abroad

        # Fetch resume
        resume_data = user_profile.get("resume")
        resume_text = extract_text_from_resume(resume_data) if resume_data else None

        return job_titles, preferred_locations, resume_text
    return [], [], None

def extract_text_from_resume(binary_resume):
    """Extracts text from a resume stored in MongoDB (Binary format)."""
    try:
        pdf_reader = PdfReader(BytesIO(binary_resume))
        text = "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
        return text
    except Exception as e:
        st.warning(f"Error extracting text from resume: {e}")
        return None

def get_job_description(job_url):
    """Fetches the full job description from the job's detail page."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={job_url}"

    try:
        response = requests.get(proxy_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            description_tag = soup.find("div", id="jobDescriptionText")
            return description_tag.get_text("\n", strip=True) if description_tag else "N/A"
    except Exception as e:
        st.warning(f"Error fetching job description: {e}")

    return "N/A"

def scrape_indeed(job_title, location, num_pages=2):
    """Scrapes Indeed job listings for a given title and location."""
    base_url = get_indeed_url(location)
    job_list = []

    for page in range(0, num_pages * 10, 10):
        url = f"{base_url}?q={job_title.replace(' ', '+')}&l={location.replace(' ', '+')}&sr=directhire&start={page}"
        proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={url}"
        headers = {"User-Agent": random.choice(USER_AGENTS)}

        try:
            response = requests.get(proxy_url, headers=headers)
            if response.status_code != 200:
                st.warning(f"Error {response.status_code} - Could not fetch {url}")
                continue
        except Exception as e:
            st.warning(f"Exception during request: {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.select("div.job_seen_beacon")

        for job in job_cards:
            title = job.select_one("h2.jobTitle a")
            title = title.get_text(strip=True) if title else "N/A"

            company = job.select_one("span.companyName")
            company = company.get_text(strip=True) if company else "N/A"

            location_tag = job.select_one("div.companyLocation")
            location = location_tag.get_text(strip=True) if location_tag else "N/A"

            job_url = job.select_one("h2.jobTitle a")
            job_url = "https://in.indeed.com" + job_url["href"] if job_url else "N/A"

            job_description = get_job_description(job_url) if job_url != "N/A" else "N/A"

            job_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Job URL": job_url,
                "Full Description": job_description
            })

        time.sleep(random.randint(2, 5))

    return job_list

def match_jobs_with_resume(resume_text, jobs, threshold=0.4):
    """Matches resume with job descriptions using AI-based similarity."""
    resume_embedding = model.encode(resume_text, convert_to_tensor=True).view(1, -1)

    matched_jobs = []
    for job in jobs:
        job_description = job["Full Description"]
        if job_description == "N/A" or len(job_description) < 50:
            continue

        job_embedding = model.encode(job_description, convert_to_tensor=True).view(1, -1)
        similarity = F.cosine_similarity(resume_embedding, job_embedding, dim=1).item()

        if similarity >= threshold:
            job["Similarity Score"] = round(similarity, 2)
            matched_jobs.append(job)

    return sorted(matched_jobs, key=lambda x: x["Similarity Score"], reverse=True)

# Streamlit UI
st.title("🎯 AI-Powered Job Finder")

job_profiles, job_locations, resume_text = fetch_user_preferences()

st.subheader("📌 Select or Enter a Job Profile")
selected_job = st.selectbox("Choose a Job Profile:", job_profiles)
custom_job = st.text_input("Or Enter a Custom Job Profile:")

st.subheader("🌍 Select a Location")
selected_location = st.selectbox("Choose a Location:", job_locations)

view_option = st.radio(
    "Choose how you want to view the jobs:",
    ("View All Jobs", "View Only Top 5 Matches")
)

if st.button("🔎 Find Jobs"):
    if not resume_text:
        st.error("No resume found in your profile. Please upload a resume in your profile settings.")
    else:
        jobs = scrape_indeed(custom_job if custom_job else selected_job, selected_location)
        matched_jobs = match_jobs_with_resume(resume_text, jobs)

        if matched_jobs:
            st.success(f"✅ Found {len(matched_jobs)} relevant jobs!")
            if view_option == "View Only Top 5 Matches":
                matched_jobs = matched_jobs[:5]

            for idx, job in enumerate(matched_jobs):
                st.write(f"**{job['Title']}** at {job['Company']} ({job['Location']})")
                st.text_area("🔗 Job URL", job["Job URL"], height=70, key=f"url_{idx}")
                st.text_area("📄 Job Description", job["Full Description"], height=200, key=f"desc_{idx}")
                st.write("---")
        else:
            st.warning("No highly relevant jobs found based on AI matching.")

st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"authenticated": False, "email": None, "full_name": None}))
