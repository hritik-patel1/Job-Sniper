from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def swiggy_scraper_jobs(driver, url):

    driver.get("https://careers.swiggy.com")

    driver.execute_script(
        "window.location.hash='#/careers?search=title:software'"
    )

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "tr.list-data"))
    )

    rows = driver.find_elements(By.CSS_SELECTOR, "tr.list-data")

    print("Rows found:", len(rows))

    jobs = []

    for row in rows:

        try:
            job_id = row.find_element(By.CSS_SELECTOR, ".mnh_req_id").text
            title = row.find_element(By.CSS_SELECTOR, ".mnh_req_title").text
            location = row.find_element(By.CSS_SELECTOR, ".mnh_location").text

            link = f"https://careers.swiggy.com/#/job/{job_id}"

            jobs.append({
                "id": job_id,
                "title": title,
                "location": location,
                "link": link
            })

        except:
            continue

    return jobs