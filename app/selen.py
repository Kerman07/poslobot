import selenium
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_jobs():
    chrome_options = webdriver.Options()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(
        executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options
    )

    baseUrl = "https://www.mojposao.ba/#!searchjobs;keyword=;page=1;title=all;range=week;location=all;i=32_31_47;lk=Sarajevo;state=all"
    driver.get(baseUrl)
    collected = []
    try:
        jobs = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "BF0HTNC-hg-l"))
        )
        for job in jobs:
            whole_link = job.find_element(By.TAG_NAME, "a")
            if whole_link.text:
                posao = whole_link.text
                whole_link = whole_link.get_attribute("href").split(";")
                link = whole_link[0] + ";" + whole_link[-1]
                hgc = job.find_elements(By.CLASS_NAME, "BF0HTNC-hg-c")[-1]
                poslodavac = hgc.text
                collected.append({posao, poslodavac, link})
    finally:
        driver.quit()
        return collected
