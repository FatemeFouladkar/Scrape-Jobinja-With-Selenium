import pandas as pd
import json
import os
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


# driver = webdriver.Chrome(executable_path='chromedriver.exe')
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def find_by_filter(title, city_fa):
    driver.get("https://jobinja.ir/jobs")
    driver.implicitly_wait(1)

    job_title = driver.find_element(By.CSS_SELECTOR, ".c-jobSearchTop__blockInput")
    job_title.send_keys(title)

    driver.find_element(By.CSS_SELECTOR, ".select2-selection__rendered").click()
    search = driver.find_element(By.CSS_SELECTOR, ".select2-search__field")
    search.send_keys(city_fa + Keys.ENTER)

    driver.find_element(By.XPATH, "//button[contains(text(),'جستجو کن')]").click()
    driver.implicitly_wait(1)
    page = 1
    cnt = 1
    output = []
    while True:
        driver.get(f'{driver.current_url}&page={page}')
        try:
            driver.find_element(By.CSS_SELECTOR, '.c-jobSearch__noResult')
            break
        except:
            results = driver.find_elements(By.XPATH, '//div[@class="o-listView__itemInfo"]')
            for r in results:
                h3_title = r.find_element(By.XPATH, './/h3/a[@class="c-jobListView__titleLink"]').text
                link = r.find_element(By.XPATH, './/h3/a[@class="c-jobListView__titleLink"]').get_attribute('href')
                company = r.find_element(By.XPATH, './/ul/li[1]/span').text
                city = r.find_element(By.XPATH, './/ul/li[2]/span').text
                job_type = r.find_element(By.XPATH, './/ul/li[3]/span/span[1]').text
                salary = r.find_element(By.XPATH, './/ul/li[3]/span/span[last()]').text

                output.append(dict({
                                "title": h3_title,
                                "company": company,
                                "city": city,
                                "job_type": job_type,
                                "salary": salary,
                                "link": link
                                }))
            cnt += 1
            page += 1    


    output_directory = f'output/{datetime.today().strftime("%Y-%m-%d")}'
    os.makedirs(output_directory, exist_ok=True)
    with open(f'{output_directory}/{title}-{city_fa}.json', 'w', encoding="utf-8") as f:
        f.write(json.dumps(output, ensure_ascii=False))
    
    df = pd.DataFrame(output) 
    df.to_csv(f"{output_directory}/{title}-{city_fa}.csv", index=False)

    driver.quit()


def login(username, password):
    driver.get("https://jobinja.ir/login/user")
    driver.find_element(By.ID, 'identifier').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password + Keys.ENTER)



login('email', 'password')
find_by_filter('title', 'city_fa')
