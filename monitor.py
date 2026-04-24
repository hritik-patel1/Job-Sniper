import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from scraper.visa_scraper import visa_scraper_jobs
from scraper.amazon_scraper import amazon_scraper_jobs
from scraper.microsoft_scraper import microsoft_scraper_jobs
from notifier import send_email
from scraper.jpmorgan_scraper import jpmorgan_scraper_jobs
from scraper.oracle_scraper import oracle_scraper_jobs
from scraper.salesforce_scraper import salesforce_scraper_jobs
from scraper.goldmansachs_scraper import goldmansachs_scraper_jobs
from scraper.paypal_scraper import paypal_scraper_jobs
from filters import company_filter
from selenium.webdriver.chrome.options import Options


# from scraper.qualcomm_scraper import qualcomm_scraper_jobs
# from scraper.swiggy_scraper import swiggy_scraper_jobs



# ---------------- CONFIG ---------------- #

SCRAPERS = {
    "amazon": amazon_scraper_jobs,
    "visa": visa_scraper_jobs,
    "microsoft": microsoft_scraper_jobs,
    "jpmorgan": jpmorgan_scraper_jobs,
    "oracle": oracle_scraper_jobs,  
    "salesforce": salesforce_scraper_jobs,
    "goldmansachs": goldmansachs_scraper_jobs,
    "paypal": paypal_scraper_jobs

    # "qualcomm": qualcomm_scraper_jobs,
    # "swiggy": swiggy_scraper_jobs,
}

# FILTERS = {
#     "amazon": amazon_filter, 
#     "visa": visa_filter,
#     "microsoft": microsoft_filter
# }


# URLS = [

#     ("https://apply.careers.microsoft.com/careers?domain=microsoft.com&query=software&start=0&location=india&pid=1970393556627119&sort_by=timestamp&filter_include_remote=1", "microsoft"),
#     ("https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi&radius=24km&latitude=28.63141&longitude=77.21676&loc_group_id=&loc_query=India&base_query=software&city=&country=IND&region=&county=&query_options=&)", "amazon"),
#     ("https://www.visa.co.uk/en_gb/jobs/?q=software&cities=Bangalore&cities=Mumbai&sortProperty=createdOn&sortOrder=DESC", "visa")
# ]

URLS = [

    ("https://apply.careers.microsoft.com/careers?domain=microsoft.com&query=software&start=0&location=india&pid=1970393556627119&sort_by=timestamp&filter_include_remote=1", "microsoft"),

    # ("https://www.amazon.jobs/en/search?offset=0&result_limit=10&sort=recent&distanceType=Mi&radius=24km&latitude=28.63141&longitude=77.21676&loc_group_id=&loc_query=India&base_query=software&city=&country=IND&region=&county=&query_options=&", "amazon"),

    # ("https://www.visa.co.uk/en_gb/jobs/?q=software&cities=Bangalore&cities=Mumbai&sortProperty=createdOn&sortOrder=DESC", "visa"),

    # ("https://jpmc.fa.oraclecloud.com/hcmUI/CandidateExperience/en/sites/CX_1001/jobs?keyword=software&location=India&locationId=300000000289360&locationLevel=country&mode=location&sortBy=POSTING_DATES_DESC", "jpmorgan"),

    # ("https://careers.oracle.com/en/sites/jobsearch/jobs?keyword=software&location=India&locationId=300000000106947&mode=location&sortBy=POSTING_DATES_DESC", "oracle"),

    # ("https://careers.salesforce.com/en/jobs/?search=software&country=India&pagesize=20#results", "salesforce"),

    # ("https://higher.gs.com/results?LOCATION=Bengaluru|Mumbai|Hyderabad&page=1&search=software&sort=POSTED_DATE", "goldmansachs"),

    # ("https://paypal.eightfold.ai/careers?query=software&start=0&location=Chennai%2C++TN%2C++India&pid=274908370246&sort_by=timestamp&filter_distance=80&filter_include_remote=1", "paypal"),

    # ("https://paypal.eightfold.ai/careers?query=software&start=0&location=Bengaluru%2C++KA%2C++India&pid=274918242550&sort_by=timestamp&filter_distance=80&filter_include_remote=1", "paypal")

    
    
    # ("https://careers.swiggy.com/#/careers?search=title:software", "swiggy"),
    # ("https://careers.qualcomm.com/careers?query=software&start=0&location=india&pid=446717281361&sort_by=timestamp&filter_include_remote=0", "qualcomm"),

]


# KEYWORDS = ["software", "developer", "engineer", "sde", "backend", "fullstack", "frontend"]
# LOCATIONS = ["india", "ind", "bengaluru", "hyderabad", "bangalore", "pune", "chennai"]

CHECK_INTERVAL = 3600   # 1 hour

SEEN_FILE = "seen_jobs.json"


# ---------------- STORAGE ---------------- #

def load_seen_jobs():
    try:
        with open(SEEN_FILE, "r") as f: 
            return set(json.load(f))
    except:
        return set()


def save_seen_jobs(seen):
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen), f)


# ---------------- FILTER ---------------- #

# def match_filters(title, location):

#     title = title.lower()
#     location = location.lower().strip()

#     keyword_match = any(k in title for k in KEYWORDS)

#     country_code = location.split(",")[0].strip()

#     location_match = country_code in LOCATIONS

#     return keyword_match and location_match


# ---------------- MAIN LOGIC ---------------- #




def run_monitor():

    seen_jobs = load_seen_jobs()
    new_jobs = []
    options = Options()

    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--remote-debugging-port=9222")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        for url, company in URLS:

            print(f"\nChecking {company}...")

            scraper = SCRAPERS[company]

            jobs = scraper(driver, url)
            jobs = jobs[:20]
            # filter_func = FILTERS[company]

            print(f"Total jobs found: {len(jobs)}")
            filtered_jobs = []
            for job in jobs:

                print("Checking job:", job["title"], "-", job["location"])

                if not company_filter(company, job["title"], job["location"]):
                    continue

                if job["id"] not in seen_jobs:

                    print("\nNEW JOB FOUND")
                    print("Company:", company)
                    print("Title:", job["title"])
                    print("Location:", job["location"])
                    print("-----------------------")

                    seen_jobs.add(job["id"])

                    job["company"] = company
                    new_jobs.append(job)
                    filtered_jobs.append(job)
            print("-----------------  Filtered jobs: ", len(filtered_jobs), "-----------------")
            print("\n".join([f"{j['title']} - {j['location']}" for j in filtered_jobs]))


        # Save updated seen jobs
        save_seen_jobs(seen_jobs)

        # Send email only if new jobs found
        if new_jobs:
            send_email(new_jobs)

    finally:
        driver.quit()
        


# ---------------- SCHEDULER ---------------- #



print("\n===== JOB CHECK STARTED =====")

run_monitor()