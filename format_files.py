import pandas as pd
import json
import requests
import numpy as np
from ast import literal_eval

def format_dataframe(df,terms):
    for term in terms:
        df[term] = df[term].apply(literal_eval)
    return df

####### First attempt at formatting the .jl file. It wasn't a success...

with open('2021-02-11T00-34-21.jl') as f:
    lines = f.read().splitlines()

df_inter = pd.DataFrame(lines)
df_inter.columns = ['json_element']
df_inter['json_element'].apply(json.loads)
df_final = pd.json_normalize(df_inter['json_element'].apply(json.loads))
df_final.to_csv('ufcFights.csv',index=False)

####### Let's take a different approach

terms = {'fighter_id','fighter_name','fighter_status','kd','n_pass',
         'n_sub','sig_str_abs','sig_str_att','sig_str_def','sig_str_land',
         'total_str_abs','total_str_att','total_str_def','total_str_land','td_abs',
         'td_att','td_def','td_land','head_abs','head_att',
         'head_def','head_land','body_abs','body_att','body_def',
         'body_land','leg_abs','leg_att','leg_def','leg_land',
         'distance_abs','distance_att','distance_def','distance_land','clinch_abs',
         'clinch_att','clinch_def','clinch_land','ground_abs','ground_att',
         'ground_def','ground_land'}

df = pd.read_csv('ufcFights.csv')
df = df.dropna() #Let's get rid of the fights with no stats
df = format_dataframe(df,terms)
df = df.apply(lambda x: x.explode() if x.name in terms else x)
df.to_csv('ufcFights_formatted.csv', index=False)