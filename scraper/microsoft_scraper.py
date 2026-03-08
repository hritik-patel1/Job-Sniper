import time
from selenium.webdriver.common.by import By


def microsoft_scraper_jobs(driver, url):

    driver.get(url)

    time.sleep(6)

    jobs = []

    job_cards = driver.find_elements(By.CSS_SELECTOR, "a.r-link.card-F1ebU")

    for card in job_cards:

        try:
            title = card.find_element(By.CSS_SELECTOR, ".title-1aNJK").text

            location = card.find_element(By.CSS_SELECTOR, ".fieldValue-3kEar").text

            link = card.get_attribute("href")

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except: 
            continue

    return jobs