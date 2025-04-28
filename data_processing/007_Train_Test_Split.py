import pand as pd 
from sklearn.model_selection import train_test_split
from umap import UMAP
from bertopic import BERTopic
from sentence_transformers import SentenceTransformer
import json 

embedding_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
umap_model = UMAP(random_state=42)

topic_model = BERTopic(
    embedding_model=embedding_model,
    umap_model=umap_model,
    calculate_probabilities=True,   
    verbose=True,
    min_topic_size=50,
    )

if __name__ == '__main__': 

    df_active = pd.read_csv('../data_clean/all_brands.csv')[['id', 'ad_delivery_start_time']]      
    df_text = pd.read_csv('../data_clean/df_text.csv')


    df_active['ad_delivery_start_year'] = pd.to_datetime(df_active['ad_delivery_start_time']).dt.year
    df_active['ad_delivery_start_month'] = pd.to_datetime(df_active['ad_delivery_start_time']).dt.month  
    df_active.drop(columns=['ad_delivery_start_time'], inplace=True)
    df_image = pd.read_csv('../data_clean/df_image2.csv').drop(columns=['ref_id', 'img_name' ])
    df_target = pd.read_csv('../data_clean/df_target.csv')
    df_text2 = df_text[['id', 'page_name', 'languages_flat', 'has_text', 'ad_creative_text_masked_clean_sw']].copy()
    df = df_active.merge(df_target, on='id', how='left')\
        .merge(df_image, on='id', how='left')\
            .merge(df_text2, on='id', how='left') 
    df = pd.get_dummies(df, columns=['languages_flat'], prefix='language')
    df = df.dropna().copy()

    map_page_name = {}
    map_page_name_num={}
    for i, brand in enumerate(list(df['page_name'].unique())):
        map_page_name[brand] =  i
        map_page_name_num[i] = brand
    map_page_name
    df['page_name_num'] = df['page_name'].map(map_page_name)

    df['target_gender_men'] = df['target_gender_men'].astype(bool).astype(int)
    df['target_gender_women'] = df['target_gender_women'].astype(bool).astype(int)

    data= df.drop(columns = ['page_name']).copy()
    X, y = data.drop(columns = 'page_name_num'), data['page_name_num']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    train_docs = X_train.loc[X_train.has_text==1, 'ad_creative_text_masked_clean_sw'].drop_duplicates().tolist()

    topics, probs = topic_model.fit_transform(train_docs)
    topic_model.get_topic_info()

    test_docs = X_test.loc[X_test.has_text==1, 'ad_creative_text_masked_clean_sw'].drop_duplicates().tolist()
    topics_test, probs_test = topic_model.transform(test_docs)

    topic_model.save("../data_clean/topic_model.pkl")

    X_train['topic_latest_armario'] = 0
    X_train['topic_maison_collection'] = 0

    # topic_map ={-1: 'other', 1:'maison_collection', 0:'latest_armario'}
    for d, p in zip(train_docs, probs):
        X_train.loc[X_train['ad_creative_text_masked_clean_sw'] == d, 'topic_latest_armario'] = p[0]
        X_train.loc[X_train['ad_creative_text_masked_clean_sw'] == d, 'topic_maison_collection'] = p[1]

    X_test['topic_latest_armario'] = 0
    X_test['topic_maison_collection'] = 0
    for d, p in zip(test_docs, probs_test):
        X_test.loc[X_test['ad_creative_text_masked_clean_sw'] == d, 'topic_latest_armario'] = p[0]
        X_test.loc[X_test['ad_creative_text_masked_clean_sw'] == d, 'topic_maison_collection'] = p[1]


    X_train = X_train.drop(columns=['ad_creative_text_masked_clean_sw'])
    X_test = X_test.drop(columns=['ad_creative_text_masked_clean_sw'])

    X_train.to_csv('../data_clean/X_train.csv', index=False)
    X_test.to_csv('../data_clean/X_test.csv', index=False)
    y_train.to_csv('../data_clean/y_train.csv', index=False)
    y_test.to_csv('../data_clean/y_test.csv', index=False)


with open("../data_clean/page_name_map.json", "w") as f:
    json.dump([map_page_name , map_page_name_num], f, indent=4)