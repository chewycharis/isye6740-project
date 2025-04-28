import pandas as pd 

if __name__ == '__main__': 
    df_target = pd.read_csv('../data_clean/all_brands.csv')[['id', 'publisher_platforms', 
                                                            'age_country_gender_reach_breakdown', 
                                                            'eu_total_reach', 'target_ages',  
                                                            'target_gender', 'target_locations']].copy()
    # platform processing 
    platforms = ['facebook', 'instagram', 'audience_network', 'messenger']
    for platform in platforms:
        df_target["publisher_platform_" + platform] = df_target['publisher_platforms'].apply(lambda x: 1 if platform in x else 0)

    # target age processing 
    df_target['target_ages'] = df_target['target_ages'].fillna("[]").apply(ast.literal_eval)
    df_target['target_ages_lower'] = df_target['target_ages'].apply(lambda x: int(x[0])  if isinstance(x, list) else None)
    df_target['target_ages_upper'] = df_target['target_ages'].apply(lambda x: int(x[1])  if isinstance(x, list) else None)

    # target gender processing
    df_target['target_gender'] = df_target['target_gender'].str.lower()
    df_target = pd.get_dummies(df_target, columns=['target_gender'], prefix='target_gender_', prefix_sep='')
    df_target.loc[df_target.target_gender_all==1, 'target_gender_men'] =1
    df_target.loc[df_target.target_gender_all==1, 'target_gender_women'] =1
    df_target = df_target.drop(columns="target_gender_all")


    publisher_platform_cols = [col for col in df_target.columns if col.startswith('publisher_platform_')]
    target_ages_cols = ["target_ages_lower","target_ages_upper"]
    target_gender_cols = ["target_gender_men", "target_gender_women"]

    df_target[["id", "eu_total_reach"] + publisher_platform_cols + target_ages_cols + target_gender_cols].head()
    df_target[["id", "eu_total_reach"] + publisher_platform_cols + target_ages_cols + target_gender_cols]\
        .to_csv("../data_clean/df_target.csv", index=False)