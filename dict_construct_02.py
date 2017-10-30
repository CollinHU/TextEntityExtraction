import csv
import pandas as pd
import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
##using lemmatizer instead of stmmer
import nltk.stem import WordNetLemmatizer

stemmer = WordNetLemmatizer()
def extract_entity(s):
    return ne_chunk(pos_tag(word_tokenize(s)))

s_level_dict = {}

def judge_subT(sub_T):
    if sub_T[:2] =='NN':
        return True;
    return False

def judge_tree(T):
    remove_list = ['PERSON','GPE']
    if T.label() in remove_list:
        return False
    return True

def traverseTree(T, num):
    for subtree in T:
        if type(subtree) == nltk.tree.Tree:
            traverseTree(subtree, num)
        else:
            if judge_subT(subtree[1]) and judge_tree(T):
                #print(T.label())
                #print(subtree[0])
                item = stemmer.lemmatize(subtree[0].lower())
                if item not in s_level_dict.keys():
                    s_level_dict[item]= [num]
                else:
                    s_level_dict[item] += [num]

s_list = pd.read_csv('data/processed_data.csv')

size = int(s_list.count().values[0])
print type(size)
count = 0
for i in xrange(size):
    s = sent_tokenize(s_list.iloc[i,1])
    print("comments :",i)
    for item in s:
        T = extract_entity(item)
        #print(T)
        traverseTree(T, i)
    count += 1
print count

with open('data/dictionary_02.csv', 'wb') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in s_level_dict.items():
            writer.writerow([key, value])


