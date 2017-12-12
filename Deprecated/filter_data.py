import pandas as pd

df = pd.read_csv('data/dictionary_01.csv',index_col = 0)
df = df[df['length'] > 10]
df.to_csv('data/dictionary_01_l10.csv')

