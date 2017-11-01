import pandas as pd
import numpy as np
import csv
import re

from nltk import wordpunct_tokenize
from nltk.corpus import words


def calculate_language_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    sen_size = len(tokens)
    #print(sen_size)
    T_words = [word.lower() for word in tokens]
    #for language in words.fileids():
    words_set = set(words.words('en'))
    T_words_set = set(T_words) 
    common_elements = T_words_set.intersection(words_set)
    ratio =float(len(common_elements))/sen_size
    return ratio

data = pd.read_csv('data/raw_data.csv',quoting=csv.QUOTE_ALL)
data.dropna(inplace = True)


comments = data['comment']
print(comments.count())
comments = comments.apply(lambda s: re.sub("\"",'',s))
comments = comments.apply(lambda s: re.sub('\n',' ',s))
comments = comments.apply(lambda s: re.sub('\s+',' ',s))
#comments.dropna()
print type(comments)

course_id = data['course_id']

#remove sentence not in english
ratio = pd.Series(np.zeros(comments.count()), index=comments.index)

col = {'course_id':course_id, 'comment':comments,'ratio':ratio}

new_data = pd.DataFrame(data=col)
new_data.dropna(inplace = True)

#calculate ratio of english words in whole sentence
new_data['ratio'] = new_data['comment'].apply(calculate_language_ratios)

#print comments['ratio']
new_data = new_data[new_data['ratio'] >= 0.5]
print(new_data.head(5))
print(new_data.count())

#new_data.drop('index',axis = 1, inplace=True)
new_data.reset_index(inplace=True)
new_data.drop('index', axis = 1, inplace = True)
new_data.to_csv('data.csv',header = True)
