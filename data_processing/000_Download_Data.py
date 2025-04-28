
import requests
from dotenv import load_dotenv
import os 
import pandas as pd 

## Brands, Countries, and Fields ## 
# Selected 10 popular luxury and more affordable brands in Europe. 
# Used each brand's most followed Meta page.
# Selected EU countries with over 10M+ populations. Only looked at EU country because of data transparency law makes more targetting data available. 
# Pulled all fields from Meta Ads library available to EU countries. 


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



luxury_brands = {
    "Chanel": 10109514234,
    "Louis Vuitton":215138065124,
    "Dior": 118197471568260,
    "Gucci": 44596321012,
    "Prada": 164637176974573,
    "Balenciaga": 128450347241247,
    "Saint Laurent (YSL)": 106537403849,
    "Versace": 260751060175,
    "Hermes": 104907696213843,
    "Burberry": 122792026424
}

more_affordable_brands={
    "H&M": 348767591942030,
    "Zara": 33331950906,
    "Bershka": 53133370935,
    "Mango": 155318785394,
    "Primark": 268505109890322,
    "Massimo Dutti": 1729151094044634,
    "Stradivarius":35320546458,
    "Pull & Bear": 96838814738, 
    "ASOS":10936503735,
    "COS": 190341761036273
}

eu_ads_fields = ["id",
"ad_snapshot_url", 
"ad_delivery_start_time", 
"ad_delivery_stop_time", 

"ad_creative_bodies",
"ad_creative_link_captions",
"ad_creative_link_descriptions",
"ad_creative_link_titles",
"languages", 

"page_id", 
"page_name",

"publisher_platforms",

"age_country_gender_reach_breakdown",
"beneficiary_payers",
"eu_total_reach",
"target_ages",
"target_gender",
"target_locations"
]


countries = ['FR', 'DE', 'IT', 'ES', 'PL', 'RO', 'NL', 'BE', 'CZ', 'PT', 'SE', 'GR']
load_dotenv()
access_token = os.getenv("META_ACCESS_TOKEN")


## Define params of API calls
# Look at up to 500 active ads for each brand 



params = {
"ad_active_status":"ALL",
"ad_reached_countries": format_fields(countries), 
"ad_type": "ALL",
"languages": "['en', 'es', 'fr', 'it', 'de']",
"media_type":"IMAGE",
"search_page_ids": [], 
"access_token": f"{access_token}",  # Replace with your valid access token
"fields" :  format_fields(eu_ads_fields),
"search_type":"page",
"limit": 500
}


if __name__ == '__main__':
 
    ## Make API calls 

    luxury_brands_df = pd.DataFrame()

    for business_name, page_id in luxury_brands.items():
        
        params['search_page_ids'] =  [page_id]
        print("getting information for", business_name)

        response = get_info(params)
        tmp_df = pd.DataFrame(response.json()['data'])

        luxury_brands_df = pd.concat((luxury_brands_df, tmp_df))

    luxury_brands_df['brand_type'] = 'luxury'


    more_affordable_brands_df = pd.DataFrame()

    for business_name, page_id in more_affordable_brands.items():

        params['search_page_ids'] =  [page_id]
        print("getting information for", business_name)

        response = get_info(params)
        tmp_df = pd.DataFrame(response.json()['data'])

        more_affordable_brands_df = pd.concat((more_affordable_brands_df, tmp_df))

    more_affordable_brands_df['brand_type'] = 'more affordable'
    brands_df = pd.concat((luxury_brands_df, more_affordable_brands_df)).reset_index()
    brands_df[brands_df.page_name !='Versace'].to_csv("../data_clean/all_brands.csv", index=False)