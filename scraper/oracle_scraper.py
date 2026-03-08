import time
from selenium.webdriver.common.by import By


def oracle_scraper_jobs(driver, url):

    driver.get(url)
    time.sleep(10)

    jobs = []

    cards = driver.find_elements(By.CSS_SELECTOR, "li[data-qa='searchResultItem']")

    for card in cards:

        try:
            title = card.find_element(By.CSS_SELECTOR, ".job-tile__title").text

            location = card.find_element(
                By.CSS_SELECTOR,
                ".job-list-item__job-info-value span"
            ).text

            link = card.find_element(
                By.CSS_SELECTOR,
                "a.job-grid-item__link"
            ).get_attribute("href")

            jobs.append({
                "id": link,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs