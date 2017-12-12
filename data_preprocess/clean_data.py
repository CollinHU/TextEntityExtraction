import pandas as pd
import re

data = pd.read_csv('../data/raw_data.csv',index_col = 0)
print("before cleaning, there are ",len(data)," comments")
def process_sentence(s):
        s = re.sub(r' \.', ' ',s)
        s = re.sub(r'=',' ',s)
        s = re.sub(r'#+',' ',s)
        s = re.sub(r'\*+',' ',s)
        s = re.sub(r'_+',' ',s)
        s = re.sub(r':+',' ',s)
        s = re.sub(r'\(+',' ',s)
        s = re.sub(r'\)+',' ',s)
        s = re.sub(r'\|+',' ',s)
        s = re.sub(r'\\\w+',' ',s)
        s = re.sub(r'/+',' ',s)
        s = re.sub(r'\\+',' ',s)
        s = re.sub(r'[^\x00-\x7f]',' ', s)
        s = re.sub(r"\"",'',s)
        s = re.sub('\n',' ',s)

        #s = re.sub(r'[[:digit:]]',' ',s)
        s = re.sub(r'\s+',' ',s)
        return s

data['comment'] = data['comment'].apply(process_sentence)
data.to_csv('../data/step1_data.csv')
print("after cleaning, there are ",len(data)," comments")
print("finish clean")
