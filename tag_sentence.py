import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk import wordpunct_tokenize
import re
from nltk.corpus import stopwords
import pandas as pd


stemmer = SnowballStemmer('english')
def tag_entity(s):
    s_list = sent_tokenize(s)
    word_list = []
    for item in s_list:
        w_list = word_tokenize(item)
        w_list = [w for w in w_list if w not in stopwords.words('english')]
        w_list = [stemmer.stem(w) for w in w_list]
        word_list += pos_tag(w_list) 
        #print(s_list)
    return word_list#ne_chunk(pos_tag(s_list))

def noun_extract(w_list):
    n_list = []
    for w in w_list:
        if w[1][:2] == 'NN':
            n_list.append(w)
    return n_list

df = pd.read_csv('data/step2_data.csv',index_col = 0)

df['tagged_sent'] = df['comment'].apply(tag_entity)
df['NN'] = df['tagged_sent'].apply(noun_extract)

df = df[['course_id','tagged_sent','NN']]
df.to_csv('data/tagged_sent.csv')
print('finished')
