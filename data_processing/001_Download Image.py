from concurrent.futures import ThreadPoolExecutor
import pandas as pd 
import os 
from selenium import webdriver
import time
import requests
from PIL import Image
from io import BytesIO
from selenium.webdriver.common.by import By

#### 
# Scrapes images off the webpages provided by Meta, which contains both image and text. 
# Also checks for duplicate images, e.g. same image, different description, and avoids downloading them to save space. 



df_image = pd.read_csv('../data_clean/all_brands.csv') [['id','ad_snapshot_url' ,'page_name']].copy()
df_image['image_url']=''
df_image['ref_id']=0

global unique_hashes
unique_hashes = {}

def dedupe_image(img, img_name, unique_imgs_path='../data_clean/unique_imgs2') -> int:
    # image_name needs to end with .png
    try:
        img_hash = hash(img.tobytes())
        
        if img_hash not in unique_hashes:
            unique_hashes[img_hash] = img_name
            unique_img_path = os.path.join(unique_imgs_path, img_name)
            img.save(unique_img_path)
            ref_id = int(img_name.split('.')[0])
        else:
            original_id = int(unique_hashes[img_hash].split('.')[0])
            ref_id = int(original_id)
            
        return ref_id 

    except Exception as e:
        print(f"Error processing image {img_name}: {e}")

def get_image_url(ad_url) -> str:
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # does not open a browser window
    driver = webdriver.Chrome(options=options)

    driver.get(ad_url)

    # Wait for page to load, without this it will fail to find the image
    time.sleep(2)

    images = driver.find_elements(By.TAG_NAME, "img")
    image_url = [img.get_attribute("src") for img in images if img.get_attribute("src")][1]

    if len(image_url) ==0:
        print("Cannot get the image url for ID", id)
        image_url = ''

    driver.quit()

    return image_url 

def download_image(image_url, id, dir = '../data_clean/unique_imgs2') -> int:
    try:
        img_data = requests.get(image_url).content
        img_obj = Image.open(BytesIO(img_data))

        return dedupe_image(img_obj, str(id)+".png", unique_imgs_path=dir)

    except:
        print("Cannot download image for ID", id)

def process_row(ind, row):
    id = row['id']
    url = row['ad_snapshot_url']
    brand = row['page_name']

    print("getting image", ind, "for brand", brand, "with id", id)

    image_url = get_image_url(url)
    df_image.loc[ind, 'image_url'] = image_url

    ref_id = download_image(image_url, id)
    df_image.loc[ind, 'ref_id'] = ref_id

if __name__ == '__main__':

# Use ThreadPoolExecutor to parallelize the processing
    chunk_size=50
    inds = list(range(0,len(df_image), chunk_size))
    for i in inds: 
        print("processing rows", i, i+chunk_size)

        with ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(lambda args: process_row(*args), df_image.iloc[i:i+chunk_size,:].iterrows())

        df_image.to_csv(f'../data_clean/df_image.csv', index=False)