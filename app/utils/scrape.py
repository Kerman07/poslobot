import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_jobs(categories, location):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"),
        chrome_options=chrome_options,
    )

    baseUrl = f"https://www.mojposao.ba/#!searchjobs;keyword=;page=1;title=all;range=week;location=all;i={categories};lk={location}"
    driver.get(baseUrl)
    driver.implicitly_wait(3)
    collected = []
    jobs = driver.find_elements(By.CLASS_NAME, "BF0HTNC-hg-l")
    for job in jobs:
        whole_link = job.find_element(By.TAG_NAME, "a")
        if whole_link.text:
            position = whole_link.text
            whole_link = whole_link.get_attribute("href").split(";")
            link = whole_link[0] + ";" + whole_link[-1]
            hgc = job.find_elements(By.CLASS_NAME, "BF0HTNC-hg-c")[-1]
            company = hgc.text
            collected.append([position, company, link])
    driver.quit()
    return collected
