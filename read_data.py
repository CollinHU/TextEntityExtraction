import pandas as pd
import numpy as np

data = pd.read_csv('test.csv')
print data.count()
comments = data['comment'].apply(lambda s: np.nan if s[:3] == '???' or len(s) == 1 else s)
comments.dropna(inplace = True)
print comments.head(20)
print(comments.count())

comments.to_csv('data.csv',index = False)
