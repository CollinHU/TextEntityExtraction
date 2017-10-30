import csv
import pandas as pd
import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer

s_level_dict = {}
stemmer = SnowballStemmer("english", ignore_stopwords=True)
def extract_entity(s):
    return ne_chunk(pos_tag(word_tokenize(s)))


def judge_subT(sub_T):
    if sub_T[:2] =='NN':
        return True;
    return False

'''def judge_tree(T):
    remove_list = ['PERSON','GPE']
    if T.label() in remove_list:
        return False
    return True
'''
def traverseTree(T, num):
    for subtree in T:
        if type(subtree) == nltk.tree.Tree:
            traverseTree(subtree, num)
        else:
            if judge_subT(subtree[1]):#and judge_tree(T):
                #print(T.label())
                #print(subtree[0])
                item = stemmer.stem(subtree[0])
                if item not in s_level_dict.keys():
                    s_level_dict[item]= [num]
                else:
                    s_level_dict[item] += [num]

s_list = pd.read_csv('data/step2_data.csv')

size = len(s_list.index.values)
print type(size)
print size
count = 0
for i in xrange(size):
    s = sent_tokenize(s_list.iloc[i,1])
#    print("comments :",i)
    for item in s:
        if len(item) == 1:
            continue
        T = extract_entity(item)
        #print(T)
        traverseTree(T, i)
    count += 1
print count

key_list = []
value_list = []
for key, value in s_level_dict.items():
    key_list.append(key)
    value_list.append(value)

dic = {'key':key_list,'id':value_list}
data = pd.DataFrame(data = dic)
data['length'] = data['id'].apply(lambda x:len(x))

data.to_csv('data/dictionary_01.csv')
data = data[data['length'] > 2]
data.to_csv('data/dictionary_01_l3.csv')


