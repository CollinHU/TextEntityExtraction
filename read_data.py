import pandas as pd
import numpy as np
import csv
import re

data = pd.read_csv('test.csv',quoting=csv.QUOTE_ALL)
#print data.count()
data['comment']= data['comment'].apply(lambda s: np.nan if s[:3] == '???' or len(s) == 1 else s)
#print type(comments)
data.dropna(inplace = True)
data.reset_index(inplace=True)

comments = data['comment']
#print comments.head(20)
print(comments.count())
comments = comments.apply(lambda s: re.sub("\"",'',s))
comments = comments.apply(lambda s: re.sub('\n',' ',s))
comments = comments.apply(lambda s: re.sub('\s+',' ',s))
comments.to_csv('data.csv')
