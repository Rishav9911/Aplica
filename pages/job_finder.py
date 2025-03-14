import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import streamlit as st
from pymongo import MongoClient
from dotenv import load_dotenv
import urllib.parse

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

# List of user-agents for rotation
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

def fetch_all_job_profiles_and_locations():
    """Fetches unique job profiles and locations from all users in MongoDB."""
    all_profiles = profiles_collection.distinct("career_preferences.preferred_profiles")
    all_locations_india = profiles_collection.distinct("career_preferences.preferred_locations_india")
    all_locations_abroad = profiles_collection.distinct("career_preferences.preferred_locations_abroad")

    all_locations = list(set(all_locations_india + all_locations_abroad))  # Combine & remove duplicates
    return sorted(all_profiles), sorted(all_locations)

def get_job_description(job_url):
    """Fetches the full job description from the job's detail page."""
    headers = {"User-Agent": random.choice(USER_AGENTS)}
    proxy_url = f"http://api.scraperapi.com/?api_key={API_KEY}&url={job_url}"

    try:
        response = requests.get(proxy_url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            description_tag = soup.find("div", id="jobDescriptionText")  # Common identifier
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
        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = requests.get(proxy_url, headers=headers)
                if response.status_code == 200:
                    break
                elif attempt == max_retries - 1:
                    st.warning(f"Error {response.status_code} - Could not fetch {url}")
                    continue
                else:
                    time.sleep(2)
            except Exception as e:
                st.warning(f"Exception during request: {e}")
                if attempt == max_retries - 1:
                    continue
                time.sleep(2)

        soup = BeautifulSoup(response.text, "html.parser")
        job_cards = soup.select("div.job_seen_beacon")

        for job in job_cards:
            title_tag = job.select_one("h2.jobTitle a") or job.select_one("a.jcs-JobTitle")
            title = title_tag.get_text(strip=True) if title_tag else "N/A"

            company_tag = job.select_one("span.companyName") or job.select_one("[data-testid='company-name']")
            company = company_tag.get_text(strip=True) if company_tag else "N/A"

            location_tag = job.select_one("div.companyLocation") or job.select_one("[data-testid='text-location']")
            location = location_tag.get_text(strip=True) if location_tag else "N/A"

            salary_tag = job.select_one("div.salary-snippet") or job.select_one("[data-testid='salary-snippet']")
            salary = salary_tag.get_text(strip=True) if salary_tag else "N/A"

            summary_tag = job.select_one("div.job-snippet") or job.select_one("[data-testid='job-snippet']")
            summary = summary_tag.get_text(strip=True) if summary_tag else "N/A"

            job_link_tag = job.select_one("h2.jobTitle a")
            job_url = "https://www.indeed.com" + job_link_tag["href"] if job_link_tag else "N/A"

            # Fetch full job description
            job_description = get_job_description(job_url) if job_url != "N/A" else "N/A"

            job_list.append({
                "Title": title,
                "Company": company,
                "Location": location,
                "Salary": salary,
                "Summary": summary,
                "Job URL": job_url,
                "Full Description": job_description
            })

        time.sleep(random.randint(2, 5))

    return job_list

def run_scraper(selected_job, selected_location, custom_job=False):
    """Runs the scraper for the selected job profile and location."""
    
    if custom_job:
        all_locations = fetch_all_job_profiles_and_locations()[1]  # Get all locations
        locations_to_search = all_locations
    else:
        locations_to_search = [selected_location]

    st.write(f"🔍 Searching for jobs for **{selected_job}** in **{', '.join(locations_to_search)}**...")
    all_jobs = []
    
    for location in locations_to_search:
        jobs = scrape_indeed(selected_job, location)
        all_jobs.extend(jobs)

    if all_jobs:
        df = pd.DataFrame(all_jobs)
        csv_filename = f"jobs_for_{st.session_state.email.replace('@', '_').replace('.', '_')}.csv"
        df.to_csv(csv_filename, index=False)
        
        st.success(f"✅ Found {len(all_jobs)} jobs! Download your results below:")
        st.download_button("📥 Download Jobs CSV", df.to_csv(index=False), file_name=csv_filename, mime="text/csv")
        
        st.header("📋 Job Listings")
        for _, row in df.iterrows():
            with st.expander(f"**{row['Title']}** at {row['Company']} ({row['Location']})"):
                st.write(f"**Salary:** {row['Salary']}")
                st.write(f"**Summary:** {row['Summary']}")
                st.write(f"**[🔗 Job Link]({row['Job URL']})**")
                st.write("### 📄 Full Description")
                st.write(row["Full Description"])

    else:
        st.warning("No jobs found based on your selection.")

# Streamlit UI
st.title("🎯 Personalized Job Finder")

job_profiles, job_locations = fetch_all_job_profiles_and_locations()

st.subheader("📌 Select or Enter a Job Profile")
selected_job = st.selectbox("Choose a Job Profile:", job_profiles)
custom_job = st.text_input("Or Enter a Custom Job Profile:")

st.subheader("🌍 Select a Location")
selected_location = st.selectbox("Choose a Location:", job_locations)

if st.button("🔎 Find Jobs"):
    run_scraper(custom_job if custom_job else selected_job, selected_location, bool(custom_job))
