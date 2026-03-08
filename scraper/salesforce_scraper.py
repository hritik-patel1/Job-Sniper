import time
from selenium.webdriver.common.by import By


def salesforce_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(5)

    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, "div.card.card-job")

    for card in cards:

        try:
            title_el = card.find_element(By.CSS_SELECTOR, "h3.card-title a")

            title = title_el.text
            link = title_el.get_attribute("href")

            location = card.find_element(
                By.CSS_SELECTOR,
                ".locations li"
            ).text

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs