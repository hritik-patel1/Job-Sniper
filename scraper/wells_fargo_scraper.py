import requests

def wells_fargo_scraper_jobs(driver, url):
    api_url = "https://www.wellsfargojobs.com/umbraco/jobboard/CandidateJobs/GetJobs"

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Referer": "https://www.wellsfargojobs.com/en/jobs/"
    }

    payload = {
        "culture": "en",
        "search": "software",
        "country": "India",
        "page": 1
    }

    response = requests.post(api_url, json=payload, headers=headers)

    print("Status:", response.status_code)
    print(response.text[:500])  # DEBUG

    if response.status_code != 200:
        print("❌ API failed")
        return []

    data = response.json()

    jobs = []

    for job in data.get("jobs", []):
        jobs.append({
            "title": job.get("title"),
            "location": job.get("location"),
            "link": "https://www.wellsfargojobs.com" + job.get("url", "")
        })

    return jobs