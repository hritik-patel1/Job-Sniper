import time
from selenium.webdriver.common.by import By


def goldmansachs_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(5)

    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, "a[href^='/roles/']")

    for card in cards:

        try:

            title = card.find_element(By.CSS_SELECTOR, "span.gs-text").text

            location = card.find_element(By.CSS_SELECTOR, "[data-testid='location']").text

            link = card.get_attribute("href")

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": "https://higher.gs.com" + link if link.startswith("/") else link
            })

        except:
            continue

    return jobs