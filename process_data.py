import pandas as pd
import re

data = pd.read_csv('data/step1_data.csv',index_col = 0)

def process_sentence(s):
    s = re.sub('(\.)+', '. ',s)
    s = re.sub(' \.', '.',s)
    s = re.sub('\"', '',s)
    s = re.sub('/', ' or ',s)
    s = re.sub('!+',' ',s)
    s = re.sub('\s+',' ',s)
    return s

data['comment'] = data['comment'].apply(process_sentence)
data.to_csv('data/step2_data.csv')
print data.head()
