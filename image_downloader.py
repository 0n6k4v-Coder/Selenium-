from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests
import io
from PIL import Image
import time
import csv

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service, options=chrome_options)

def search_google(search_query):
    search_url = f"https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q={search_query}"

    browser = webdriver.Chrome(service=service, options=chrome_options)
    browser.get(search_url)
    browser.maximize_window()

    time.sleep(3)

    image_urls = []

    count = 0
    for i in range(0, 10):
        count += 1

        try:
            # คลิกที่รูปภาพ
            img_box = browser.find_elements(By.CSS_SELECTOR, 'div[jsname="dTDiAc"]')[i]
            img_box.click()
            time.sleep(10)

            # ดึงลิงก์รูปภาพ
            img_box_2 = browser.find_elements(By.CSS_SELECTOR, 'div[jsname="figiqf"]')[1]
            link = img_box_2.find_elements(By.TAG_NAME, 'img')[0].get_attribute('src')

            # เก็บ link ไว้ใน image_urls
            image_urls.append(link)
            print(f"Scrap Image_URLS Success for image {i+1}")

        except Exception as e:
            print(f"Error at index {i}: {e}")
            pass

    browser.close()

    return image_urls

def download_image(download_path, url, file_name):
    try:
        image_content = requests.get(url).content
        image_file = io.BytesIO(image_content)
        image = Image.open(image_file)
        file_path = download_path + file_name

        with open(file_path, "wb") as f:
            image.save(f, "JPEG")

        print(f"Downloaded {file_name} successfully")
    except Exception as e:
        print('FAILED -', e)

# เรียกใช้งานฟังก์ชัน
image_urls = search_google("เลย์")

# วนลูปดาวน์โหลดรูปภาพโดยใช้ชื่อไฟล์ lays.[i].jpeg
download_path = 'lays_images'  # ระบุโฟลเดอร์ที่ต้องการบันทึกภาพ
for i, url in enumerate(image_urls):
    file_name = f'lays.{i+1}.jpeg'  # ตั้งชื่อไฟล์เป็น lays.[i].jpeg
    download_image(download_path, url, file_name)