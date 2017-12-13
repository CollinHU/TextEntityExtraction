import pandas as pd
import numpy as np
import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import wordpunct_tokenize
import re
from nltk.corpus import stopwords
import pandas as pd
import json

def matching(key_one, key_two):
    key_one_list = word_tokenize(key_one)
    key_two_list = word_tokenize(key_two)
    if key_two_list[:2] == key_one_list or key_two_list[-2:] == key_one_list:
        return True
    else:
        return False

summary_file = "course_meQ0ic9uEeWu4RLrx6VBYw"
filtered_summary = "../result/{}_target_filtered.txt".format(summary_file)
summary_file = "../result/"+ summary_file + "_transaction.csv"

transaction = pd.read_csv(summary_file,index_col = 0)
df_size = len(transaction)

targets = transaction['target'].values

size = len(targets)
threshold = int(0.01*size)
phrase_threshold = 0
if size > 300:
    phrase_threshold = 1

G_dict = {}
for i in range(size):
    L_dict = eval(targets[i])
    for key in L_dict.keys():
        if len(key) > 1:
            G_dict[key] = G_dict.get(key, 0) + 1


new_dict = {}
for key in G_dict.keys():
    tk_key = nltk.word_tokenize(key)
    if len(tk_key) < 3:
        new_dict[key] = G_dict[key]

for key in G_dict.keys():
    tk_key = nltk.word_tokenize(key)
    flag = False
    if len(tk_key) > 2:
        for new_key in new_dict.keys():
            if len(word_tokenize(new_key)) == 2:
                flag = matching(new_key, key)
            if flag:
                new_dict[new_key] += G_dict[key]
                break      
        if flag == False:
            new_dict[key] = G_dict[key]

filter_dict = {}
for key in new_dict.keys():
    if len(word_tokenize(key)) > 1 and G_dict[key] > phrase_threshold:
        filter_dict[key] = G_dict[key]
    elif new_dict[key] > threshold:
        filter_dict[key] = new_dict[key]
print(len(filter_dict))

with open(filtered_summary, 'w') as f:
    f.write(json.dumps(filter_dict))
print('finished..')