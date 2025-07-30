from bs4 import BeautifulSoup
from selenium import webdriver
import time

driver = webdriver.Chrome()

def scrolldown(driver, deep):
    for _ in range(deep):
        driver.execute_script("window.scrollBy(0, 500)")
        time.sleep(0.2)

def get_info(driver, url):
    driver.get(url)
    scrolldown(driver, 30)
    main_page_html = BeautifulSoup(driver.page_source, "html.parser")

    content=main_page_html.find_all("div", {"class": "tn-atom"})
    text = " ".join([el.get_text(separator=" ", strip=True) for el in content])
    return text






















