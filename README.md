# ISYE6740 Final Project: What's in a Brand? 👔💄✨
## An analysis of digital ads from 20 fashion brands in the EU 
ChuHui Fu, April 27, 2025

## Introduction 
In this project, we will explore fashion ads on Meta platforms, some of the most popular channels for digital marketing. While the ads posted there might not be specifically designated for brand marketing, they still tell a story about how these company portray themselves holistically and to each customer segment.

Broadly speaking, we are trying to understand how fashion companies portray themselves through their digital ads, and how their approach differ for each target audience, by addressing the following questions: 

- What elements of ads does a company use to portray its brand?
- Do each company's ads have a distinctive enough style that differentiates them from those of its competitors? 
- How does a company adjust its messages and visuals for different demographics?

Detailed discussions can be found in the [final term paper here.](https://drive.google.com/file/d/1wCtIEshNq-VQwicHkNS2hVU1XvXWrR3E/view?usp=sharing) 

## Data Source 
For our analysis, we used the data from the Meta Ads Library, which is a publicly accessible repository with information about ads running across all of Meta's platforms, including Facebook, Instagram, Messenger, Threads, and Audience Network. To comply with the Digital Services Act (DSA) of 2022, the repository contains information on ad delivery timing, ad creatives (e.g. pictures), publisher platforms, beneficiary payers, reach, as well as targeting information by age, gender and location, for all EU ads on its platforms, dating back to 1 year after the day that the ads stop running.  

## Methodology
To ensure the scope of work is feasible, we only looked into image ads from 20+ popular fashion companies in the EU, using each company's most followed Meta account, and only included their ads delivered to the top EU countries with over 10M+ populations. We selected fashion companies that differ in terms of affordability and demographic targets.  All code for methods mentioned in this section can be found in this GitHub repository; due to copyrights and Meta data retention policy, ads data will not be released.  

### Data Collection 
Practically speaking, we collected data through the Meta Ads Library API in April 2025, and used the provided media links to scrape all creative assets with the Selenium python package. We collected 3,761 ads including both active and inactive ones, which contain 1,171 unique images. Next we performed unstructured data processing. 

### Image Processing 
For images, we performed color analysis with clustering algorithms (e.g. KMeans) to identify dominant colors of the ads and represent them in RBG values; additionally, we calculated background entropy on edges of the image to measure the complexity of the image background; lastly, we performed object detection with pre-trained models (e.g. YOLO, DETR) to identify if a person is present in the ads. 

### Sentence Processing 
For sentences in the ads description, we attempted to translate all of them to English but found that the translation quality was low due to descriptions having mixed languages. Therefore, while we still removed stop words using language-specific spaCy models (e.g. core_web_sm for English and core_news_sm for Spanish, German, Italian, and French) to obtain meaningful tokens, we moved to using topic modeling (e.g. BERTopic with embedding model paraphrase-multilingual-MiniLM-L12-v2 ) and set the topic probability as our sentence representation.  

### Data Analysis 
For analysis, we focused on addressing each of our questions, and developed a deeper understanding of the results through a combination of exploratory data analysis and online research.

For more details, read [final term paper here.](https://drive.google.com/file/d/1wCtIEshNq-VQwicHkNS2hVU1XvXWrR3E/view?usp=sharing) 

## Installation

1. Pull repo and install requirements 
```bash
git clone https://github.com/chewycharis/isye6740-project.git
conda create --name myenv python=3.10
conda activate myenv
pip install -r requirements.txt
```
3. Run python scripts data_processing folder 
4. Run notebook in notebook_clean folder 

 




