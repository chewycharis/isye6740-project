import requests
from dotenv import load_dotenv
import os 
import pandas as pd 
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def get_info(params):

    api_version = "v22.0"  
    url = f"https://graph.facebook.com/{api_version}/ads_archive"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        print("Request Successful!")
        return(response) 
    else:
        print(f"Request Failed! Status Code: {response.status_code}")
        return(response.text)  

def format_fields(fields): 
    return "["+ ",".join(["'" + x + "'" for x in fields])+"]"

def get_image_url(ad_url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in the background
    driver = webdriver.Chrome(options=options)

    driver.get(ad_url)

    # Wait for page to load
    time.sleep(2)

    # Find all ad images
    images = driver.find_elements(By.TAG_NAME, "img")
    image_url = [img.get_attribute("src") for img in images if img.get_attribute("src")][1]

    if len(image_url) ==0:
        print("Cannot get the image url for ID", id)
        image_url = ''

    driver.quit()

    return image_url 

def download_image(image_url, id, dir = "imgs"):
    try:
        img_data = requests.get(image_url).content
        img_obj = Image.open(BytesIO(img_data))

        file_name = os.path.join(dir, str(id)+".png")
        img_obj.save(file_name)
    except:
        print("Cannot download image for ID", id)



