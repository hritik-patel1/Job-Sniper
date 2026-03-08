import time
from selenium.webdriver.common.by import By


def paypal_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(6)

    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, 'div[data-test-id="job-listing"]')

    for card in cards:

        try:
            title = card.find_element(By.CSS_SELECTOR, ".title-1aNJK").text

            location = card.find_element(By.CSS_SELECTOR, ".fieldValue-3kEar").text

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