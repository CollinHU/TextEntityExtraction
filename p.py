import pandas as pd
name = 'data/dictionary_02_l3.csv'
df = pd.read_csv(name,index_col=0)

df = df[['key','length','id']]

df.to_csv(name)
