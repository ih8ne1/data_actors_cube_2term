from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
import re


options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# url = "https://www.kino-teatr.ru/teatr/acter/all/ros/a/"
# driver.get(url)
# sleep(5)
# wait = WebDriverWait(driver, 30)

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
from time import sleep

def gather_data(driver):
    name_elements = driver.find_elements(By.CLASS_NAME, "list_item_name")
    data = {}
    for idx, element in enumerate(name_elements, start=1):
        link_element = element.find_element(By.TAG_NAME, "a")
        name = link_element.text.strip()
        href = link_element.get_attribute("href")
        data[idx] = {'name': name, 'href': href}
    return data

def get_data_from_profile(driver, href):
    driver.get(href)
    try:
        date_of_birth_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div/div[2]/div[2]/div[1]/div[1]/div[2]/div[2]/span"))
        )
        date_of_birth = date_of_birth_element.text.strip()
    except:
        date_of_birth = "0000 00 00"
    
    try:
        additional_text_element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div[4]/div/div[2]/div[2]/div[1]/div[5]/div[2]"))
        )
        additional_text = additional_text_element.text.strip()
    except:
        additional_text = ""
    
    return date_of_birth, additional_text

def extract_theatre_works(additional_text):
    # Находим индекс начала информации о театральных работах
    start_index = additional_text.find('ТЕАТРАЛЬНЫЕ РАБОТЫ')
    # Если информация о театральных работах присутствует, извлекаем ее
    if start_index != -1:
        theatre_works = additional_text[start_index:]
        # Удаляем заголовок 'ТЕАТРАЛЬНЫЕ РАБОТЫ'
        theatre_works = theatre_works.replace('ТЕАТРАЛЬНЫЕ РАБОТЫ', '').strip()
        return theatre_works
    # Если информация о театральных работах отсутствует, возвращаем пустую строку
    else:
        return ''

def extract_quoted_text(text):
    pattern = r'«(.*?)»'
    matches = re.findall(pattern, text)
    return matches

driver = webdriver.Chrome()
url = "https://www.kino-teatr.ru/teatr/acter/all/ros/a/"
driver.get(url)

data_with_dob = {}
data_with_dob1 = {}

# Проверка, существуют ли файлы, и загрузите их содержимое
if os.path.exists('collected_data_with_dob.json'):
    with open('collected_data_with_dob.json', 'r', encoding='utf-8') as json_file:
        try:
            data_with_dob = json.load(json_file)
        except json.JSONDecodeError:
            data_with_dob = {}

if os.path.exists('collected_data_with_dob1.json'):
    with open('collected_data_with_dob1.json', 'r', encoding='utf-8') as json_file:
        try:
            data_with_dob1 = json.load(json_file)
        except json.JSONDecodeError:
            data_with_dob1 = {}

num_pages = 2

for page in range(1, num_pages + 1):
    print(f"Scraping data from page {page}...")
    
    data_all = gather_data(driver)
    
    for idx, info in data_all.items():
        unique_id = f"{page}_{idx}" 
        date_of_birth, additional_text = get_data_from_profile(driver, info['href'])
        data_with_dob[unique_id] = {'name': info['name'], 'href': info['href'], 'date_of_birth': date_of_birth, 'additional_text': additional_text}
        data_with_dob1[unique_id] = {'name': info['name'], 'date_of_birth': date_of_birth, 'theatre_works': extract_quoted_text(extract_theatre_works(additional_text))}
        sleep(5)
    
    if page < num_pages:
        next_page_url = f"https://www.kino-teatr.ru/teatr/acter/m/ros/a/a{page+1}/"
        driver.get(next_page_url)
    sleep(3)

with open('collected_data_with_dob.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_with_dob, json_file, indent=4, ensure_ascii=False)

with open('collected_data_with_dob1.json', 'w', encoding='utf-8') as json_file:
    json.dump(data_with_dob1, json_file, indent=4, ensure_ascii=False)

print("Data saved to collected_data_with_dob.json")
driver.quit()