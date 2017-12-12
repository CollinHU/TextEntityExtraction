import pandas as pd

import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import wordpunct_tokenize
#import re
from nltk.corpus import stopwords
from clean_data import process_sentence

##2017 12 3 using a different parser to parse sentence
'''
from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = '/Users/collin/stanford/stanford-parser-full-2017-06-09/stanford-parser.jar'
path_to_models_jar = '/Users/collin/stanford/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
'''

from nltk.parse.corenlp import CoreNLPServer, CoreNLPDependencyParser
path_to_jar = '/Users/collin/stanford/stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0.jar'
path_to_models_jar = '/Users/collin/stanford/stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0-models.jar'
server = CoreNLPServer(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
server.start()
dependency_parser = CoreNLPDependencyParser()


stemmer = SnowballStemmer('english')
def stem(w):
    return stemmer.stem(w)

DR_one = ['nsubj','dobj','xsubj','csubj','nmod','iobj','xcomp']
DR_two = ['amod']
#DR_two = ['nsubj','dobj','xsubj','csubj','nsubjpass','nmod','iobj']
DR_three = ['conj']
DR = DR_one + DR_three

def extract_rule(dep_dic):
    value_list = []
    one_list = []
    three_list = []
    for key,value in dep_dic.items():
        if key in DR_one:
            one_list += value
        elif key in DR_two:
            three_list += value
    value_list.append(one_list)
    value_list.append(three_list)      
    return value_list

def dict_add(dic, key, value):
    if key in dic.keys():
        dic[key].append(value)
    else:
        dic[key] = [value]

def gather_target_opinion(s):
    opinion_dict = {}
    target_dict = {}
    ##parse the sentence
    result = dependency_parser.raw_parse(s)
    dep = next(result)
    dep_list = dict(sorted(dep.nodes.items()))

    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
                w = stem(node['word'])
                if w in opinion_list and node['tag'][:2] == 'JJ':
                    dict_add(opinion_dict, w, node['word'])
                elif w in target_list and node['tag'][:2] == 'NN':
                    dict_add(target_dict, w, node['word'])
                #
    return target_dict,opinion_dict


def merge_dict(d1,d2):
    for key, value in d1.items():
        if key in d2.keys():
            d2[key] += value
        else:
            d2[key] = value
    return d2


def parse_comment(sents):
    target_d = {}
    opinion_d = {}
    sent_list = sent_tokenize(sents)
    for sent in sent_list:
        tar, op = gather_target_opinion(sent)
        target_d = merge_dict(tar, target_d)
        opinion_d = merge_dict(op,opinion_d)
    return target_d, opinion_d

f1 = open('opinion_list_1.txt','r')
lines = f1.readlines()
opinion_list =[line.split("\n")[0] for line in lines]

f2 = open('target_list_1.txt','r')
lines = f2.readlines()
target_list = [line.split("\n")[0] for line in lines]

print(opinion_list)
print(target_list)

df = pd.read_csv('data.csv', index_col = 0)
df['comment'] = df['comment'].apply(process_sentence)
#print(df.head())
print(len(df.index.values))

#opinion_size = len(opinion_list)
#target_size = len(target_list)

sents = df['comment'].values
opinion_d_l = []
target_d_l = []
for sent in sents:
    tp, op =parse_comment(sent)
    opinion_d_l.append(op)
    target_d_l.append(tp)
#print(opinion_d_l)

dict_list = {'opinion': [], 'target': []}
dict_list['opinion'] = opinion_d_l
dict_list['target'] = target_d_l
df = pd.DataFrame(data = dict_list)
df.head()
server.stop()
df.to_csv('transactions.csv')
