import csv
import pandas as pd
import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.metrics.distance import edit_distance

max_dist = 1
def fuzzy_match(w1,w2):
    return edit_distance(w1,w2) <= max_dist

def match_key(w_list, key):
    for w in w_list:
        if fuzzy_match(w,key):
            return True
    return False

merged_key_dict = {}
s_list = pd.read_csv('data/dictionary_01.csv')

key_list = s_list['key'].values
merged_key_dict[key_list[0]] = [key_list[0]]

for item in key_list[1:]:
    is_not_key = True
    for k in merged_key_dict.keys():
        if match_key(merged_key_dict[k],item):
            merged_key_dict[k].append(item)
            is_key = False
            break
    if(is_not_key):
        merged_key_dict[item] = [item]

df_key = []
df_key_list = []
for key, value in merged_key_dict.items():
    df_key.append(key)
    df_key_list.append(value)

df_dic = {'key':df_key,'key_list':df_key_list}
df = pd.DataFrame(df_dic)
df.to_csv('test.csv')
print 'finished'
