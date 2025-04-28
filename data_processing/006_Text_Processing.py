import pandas as pd 
import re 
import spacy


def remove_punctuation_and_whitespace(text):
    # Remove punctuation and special characters
    text = re.sub(r'[^\w\s]', '', text)
    text = text.replace('\n', ' ').replace('\t', ' ')
    return text.strip()

#load language models
nlp_en = spacy.load("en_core_web_sm")
nlp_es = spacy.load("es_core_news_sm")
nlp_de = spacy.load("de_core_news_sm")
nlp_it = spacy.load("it_core_news_sm")
nlp_fr = spacy.load("fr_core_news_sm")
nlp_models = {"it": nlp_it, "es": nlp_es, "de": nlp_de, "fr": nlp_fr, "en": nlp_en}


def remove_stopwords(row):
    language = row['languages_flat']
    text=row['ad_creative_text_masked_clean']
    if language in nlp_models and len(text) > 0:
        nlp = nlp_models[language]
        doc = nlp(text)
        clean_text = " ".join([token.text for token in doc if not token.is_stop])
    else:
        clean_text = text
    return clean_text


if __name__ == '__main__': 

    df_text = pd.read_csv('../data_clean/all_brands.csv')[["id", "ad_creative_bodies", "ad_creative_link_descriptions",
                        "ad_creative_link_titles", "languages","page_name"]]

    # change text entries from list to string
    df_text['ad_creative_bodies_flat'] = df_text['ad_creative_bodies'].fillna("[]").apply(ast.literal_eval)
    df_text['ad_creative_bodies_flat'] = df_text['ad_creative_bodies_flat'].apply(lambda x: " ".join(x) if isinstance(x, list) else x)
    df_text['ad_creative_link_descriptions_flat'] = df_text['ad_creative_link_descriptions'].fillna("[]").apply(ast.literal_eval)
    df_text['ad_creative_link_descriptions_flat'] = df_text['ad_creative_link_descriptions_flat'].apply(lambda x: " ".join(x) if isinstance(x, list) else x)
    df_text['ad_creative_link_titles_flat'] = df_text['ad_creative_link_titles'].fillna("[]").apply(ast.literal_eval)
    df_text['ad_creative_link_titles_flat'] = df_text['ad_creative_link_titles_flat'].apply(lambda x: " ".join(x) if isinstance(x, list) else x)
    df_text['languages_flat'] = df_text['languages'].fillna("[]").apply(ast.literal_eval)
    df_text['languages_flat'] = df_text['languages_flat'].apply(lambda x: x[0] )

    # combine all the text fields into one column
    df_text['ad_creative_text'] = df_text['ad_creative_link_titles_flat'] + " " + df_text['ad_creative_bodies_flat'] + " " + df_text['ad_creative_link_descriptions_flat']

    # remove all brand names from the text
    df_text['ad_creative_text_masked']  = df_text.apply(lambda x: x['ad_creative_text'].lower().replace(x['page_name'].lower(), ''), axis=1)
    # some brand names have no space in between brand names like louisvuitton showing up as one word
    df_text['ad_creative_text_masked']  = df_text.apply(lambda x: x['ad_creative_text_masked'].lower().replace(x['page_name'].lower().replace(" ",""), ''), axis=1)

    df_text = df_text[["id", "page_name", "languages_flat", "ad_creative_text_masked"]].copy()


    df_text['ad_creative_text_masked_clean'] = df_text['ad_creative_text_masked']\
            .apply(lambda x: remove_punctuation_and_whitespace(x) if not pd.isna(x) else x)
    df_text['has_text'] = df_text['ad_creative_text_masked_clean'].apply(lambda x: 1 if len(x) > 0 else 0)
    df_text['ref_id'] = df_text['id'].copy()
    df_text['ad_creative_text_masked_clean_sw'] = df_text.apply(remove_stopwords, axis=1)
    df_text[['id', 'page_name', 'languages_flat', 'has_text', 'ad_creative_text_masked_clean_sw']]\
        .to_csv('../data_clean/df_text.csv', index=False)