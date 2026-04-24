import argparse
import importlib
from selenium import webdriver
from webdriver_manager.chromium import ChromiumDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def main():
    parser = argparse.ArgumentParser(description='Test a single company scraper')
    parser.add_argument('company', help='Company name (e.g., amazon)')
    parser.add_argument('url', help='URL to scrape')
    args = parser.parse_args()

    company = args.company
    url = args.url

    # Dynamically import the scraper module
    try:
        scraper_module = importlib.import_module(f'scraper.{company}_scraper')
        scraper_func = getattr(scraper_module, f'{company}_scraper_jobs')
    except (ImportError, AttributeError) as e:
        print(f"Error importing scraper for {company}: {e}")
        return

    # Set up headless Chrome driver
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chromium(service=service, options=options)

    try:
        print(f"Testing scraper for {company} with URL: {url}")
        jobs = scraper_func(driver, url)
        print(f"Found {len(jobs)} jobs:")
        for job in jobs[:10]:  # Limit output to first 10
            print(f"- {job['title']} | {job['location']} | {job['link']}")
        if len(jobs) > 10:
            print(f"... and {len(jobs) - 10} more")
    except Exception as e:
        print(f"Error running scraper: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()