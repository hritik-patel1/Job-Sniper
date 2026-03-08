
import time
from selenium.webdriver.common.by import By
def visa_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(5)

    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, "li.vs-underline")
    

    for card in job_cards:

        try:
            title = card.find_element(By.CSS_SELECTOR, "a.vs-link-job").text

            link = card.find_element(By.CSS_SELECTOR, "a.vs-link-job").get_attribute("href")

            location_raw = card.find_element(By.CSS_SELECTOR, ".vs-listing-description p").text
            location = location_raw.replace("Location", "").strip()

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs[:20]