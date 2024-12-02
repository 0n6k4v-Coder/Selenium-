from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import io
from PIL import Image
import time

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

def search_gettyimages(search_query):
    search_url = f"https://www.gettyimages.com/search/2/image-film?family=creative&phrase={search_query}"

    driver.get(search_url)
    driver.maximize_window()

    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.vItTTzk8rQvUIXjdVfi4')))

    image_urls = []

    count = 0
    for i in range(0, 10):
        count += 1

        try:
            # คลิกที่กล่องรูปภาพ
            img_box = driver.find_elements(By.CSS_SELECTOR, 'div.vItTTzk8rQvUIXjdVfi4')[i]
            img_box.click()

            # Wait for image to load after click
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'figure.fm5xLZr6E1NLQUhYh_xd')))
            
            # Get the image URL
            img_element = driver.find_element(By.CSS_SELECTOR, 'figure.fm5xLZr6E1NLQUhYh_xd img.BLA_wBUJrga_SkfJ8won')
            link = img_element.get_attribute('src')

            # Add image URL to the list
            image_urls.append(link)
            print(f"Scrap Image_URLS Success for image {i+1}")

        except Exception as e:
            print(f"Error at index {i}: {e}")
            pass

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = f"{download_path}/{file_name}"

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Downloaded {file_name} successfully")
    except Exception as e:
        print('FAILED -', e)

# เรียกใช้งานฟังก์ชัน
image_urls = search_gettyimages("Ammo 9mm Parabellum")

# วนลูปดาวน์โหลดรูปภาพโดยใช้ชื่อไฟล์ lays.[i].jpeg
download_path = 'lays_images'  # ระบุโฟลเดอร์ที่ต้องการบันทึกภาพ
for i, url in enumerate(image_urls):
    file_name = f'lays.{i+1}.jpeg'  # ตั้งชื่อไฟล์เป็น lays.[i].jpeg
    download_image(download_path, url, file_name)
