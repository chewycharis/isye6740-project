import pandas as pd 
from sklearn.cluster import KMeans 
from collections import Counter
from PIL import Image
import os 
from transformers import DetrImageProcessor, DetrForObjectDetection
import torch
import numpy as np 
from skimage.color import rgb2gray
from skimage.filters import rank
from skimage.morphology import disk
from skimage import  util

df_image = pd.read_csv('../data_clean/df_image.csv')
df_image2 = df_image[['id','ref_id']].copy()
df_image2['img_name'] = df_image2['ref_id'].astype(str) + '.png'

# dominant colors 
def get_top_dominant_colors(image, top_n=3):
    img_array = np.array(image)
    pixels = img_array.reshape(-1, 3)
    kmeans = KMeans(n_clusters=top_n, random_state=42)
    kmeans.fit(pixels)
    colors = kmeans.cluster_centers_.astype(int)
    counts = Counter(kmeans.labels_)
    sorted_colors = sorted(zip(colors, counts.values()), key=lambda x: x[1], reverse=True)
    return [color for color, _ in sorted_colors]

# detect person 
def detect_person(img_path): 
    image = Image.open(img_path)
    processor = DetrImageProcessor.from_pretrained("facebook/detr-resnet-50")
    model = DetrForObjectDetection.from_pretrained("facebook/detr-resnet-50")
    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes=target_sizes, threshold=0.6)[0]

    try:
        labels = results['labels'].tolist()
        if 1 in labels:
            return 1
        else:
            return 0
    except:
        return 0

# background entropy 
def background_entropy(img_path, border_width=10, dir='../data_clean/unique_imgs2/'):
    try: 
        img = Image.open(os.path.join(dir, img_path))
        w, h = img.size
        w = min(w,h)
        img = img.resize((w,w))  
        gray = rgb2gray(img)
        gray = util.img_as_ubyte(gray)
        entropy_img = rank.entropy(gray, disk(5))
        top = entropy_img[:border_width, :]
        bottom = entropy_img[-border_width:, :].reshape(top.shape)
        left = entropy_img[:, :border_width].reshape(top.shape)
        right = entropy_img[:, -border_width:].reshape(top.shape)
        border_entropy = np.mean(np.concatenate([top, bottom, left, right], axis=None))
        return border_entropy
    except: 
        return None




if __name__ == '__main__':

    unique_imgs_path = '../data_clean/unique_imgs2/'
    img_color_list =  os.listdir(unique_imgs_path)

    for img_name in img_color_list:
        img_path_full = os.path.join(unique_imgs_path, img_name)
        image = Image.open(img_path_full) 
        print("getting colors for image", img_name)
        try:
            top_colors = get_top_dominant_colors(image, top_n=3)

            for i, color in enumerate(top_colors):
                r, g, b = color
                df_image2.loc[df_image2['img_name'] == img_name, f'r{i+1}'] = r
                df_image2.loc[df_image2['img_name'] == img_name, f'g{i+1}'] = g
                df_image2.loc[df_image2['img_name'] == img_name, f'b{i+1}'] = b
        except ValueError as e:
            print(f"Error processing image {img_name}: {e}")


    for i, img_name in enumerate(img_color_list):
        print(f'Processing {i+1}/{len(img_color_list)}: {img_name}')
        try:
            img_path_full = os.path.join(unique_imgs_path, img_name)
            person_ind = detect_person(img_path_full)
            df_image2.loc[df_image2['img_name'] == img_name, 'has_person'] = person_ind
        except ValueError as e:
            print(f"Error processing image {img_name}: {e}")
    
    df_image2['background_entropy'] = df_image2['img_name'].apply(background_entropy)
    df_image2.to_csv('../data_clean/df_image2.csv', index=False)