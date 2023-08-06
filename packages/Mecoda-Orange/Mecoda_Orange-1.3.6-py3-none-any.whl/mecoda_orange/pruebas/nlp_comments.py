import pandas as pd
import requests
import pandas as pd
import numpy as np
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_odor_list():
    base_api = "https://odourcollect.eu/api"
    url = f"{base_api}/odor/list"
    odour_list = requests.get(url).json()['content']
    df = pd.DataFrame(odour_list)
    return df

def get_comments_origins(df):
    comments = {}
    origins = {}

    for id_ in df['id']:
        print(id_)
        try:
            comment = requests.get(f"https://odourcollect.eu/api/odor/{id_}").json()['object']['description']
            origin = requests.get(f"https://odourcollect.eu/api/odor/{id_}").json()['object']['origin']

            if origin is not None:
                origins[id_] = origin
            else:
                origins[id_] = np.nan
            
            if comment is not None:
                comments[id_] = comment
            else:
                comments[id_] = np.nan

        except:
            origins[id_] = np.nan
            comments[id_] = np.nan

    df['comments'] = df['id'].apply(lambda x: comments[x])
    df['origin'] = df['id'].apply(lambda x: origins[x])
    
    return df

df = get_odor_list()
df_full = get_comments_origins(df)

df_comments = df_full[df_full['comments'].notnull()]
df_comments = df_comments[['id', 'comments']]

sid = SentimentIntensityAnalyzer()

df_comments[['neg', 'neu', 'pos', 'compound']] = df_comments['comments'].apply(sid.polarity_scores).apply(pd.Series)

df_comments.to_csv("odour_collect_20220428_sentiment_analysis.csv", index=False)

