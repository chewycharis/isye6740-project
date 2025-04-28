import pandas as pd 
import ast

if __name__ == '__main__': 

    df_breakdown = pd.read_csv('../data_clean/df_target')[['id', 'age_country_gender_reach_breakdown']]
    df_breakdown['age_country_gender_reach_breakdown'] = df_breakdown['age_country_gender_reach_breakdown'].apply(ast.literal_eval)
    df_breakdown['country'] =df_breakdown['age_country_gender_reach_breakdown'].apply(lambda x: x[0]['country'] if isinstance(x, list) else None)

    df_reach = pd.DataFrame()
    for i, row in df_breakdown.iterrows():
        tmp_df = pd.DataFrame(row['age_country_gender_reach_breakdown'][0]['age_gender_breakdowns'])
        tmp_df['id'] = row['id']
        tmp_df['country'] = row['country']
        df_reach = pd.concat([df_reach, tmp_df])

    df_reach[['male','female','unknown']] = df_reach[['male','female','unknown']].fillna(0).astype(int)
    df_reach.to_csv('../data_clean/df_reach.csv', index=False)