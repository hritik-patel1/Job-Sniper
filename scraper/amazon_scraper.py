
import time
from selenium.webdriver.common.by import By

def amazon_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(5)

    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, ".job-tile")

    for card in job_cards:
        try:

            title = card.find_element(By.CSS_SELECTOR, "h3").text

            location_raw = card.find_element(By.CSS_SELECTOR, ".location-and-id").text
            location = location_raw.split("\n")[0].strip()

            link = card.find_element(By.CSS_SELECTOR, "a").get_attribute("href")

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs