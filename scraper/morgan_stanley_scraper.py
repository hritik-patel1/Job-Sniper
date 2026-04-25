import time
from selenium.webdriver.common.by import By


def morgan_stanley_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(6)

    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'a[id*="job-card"]')

    for card in job_cards:

        try:
            title = card.find_element(By.CSS_SELECTOR, ".title-1aNJK").text

            location = card.find_element(By.CSS_SELECTOR, ".fieldValue-3kEar").text

            link = card.get_attribute("href")
            
            # Convert relative link to absolute
            if link.startswith("/"):
                link = "https://morganstanley.eightfold.ai" + link

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs
