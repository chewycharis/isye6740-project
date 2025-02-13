import requests
import os 
import pandas as pd 
from PIL import Image
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from util import get_image_url, download_image


df = pd.read_csv("active_brands.csv")
df = df.drop(columns=["index", df.columns[0]])



## Get image url and download image locally. 
# Images will not be distributed, and will be deleted within 90 days of download
 
df['image_url']=''
os.makedirs('imgs', exist_ok=True)

for ind, row in df.iloc.iterrows():

    id = row['id']
    url =row['ad_snapshot_url']
    brand = row['page_name']

    print("getting image", ind, "for id", id)
    
    image_url = get_image_url(url)
    df.loc[ind, 'image_url'] = image_url 

    download_image(image_url, id, dir = "imgs")


