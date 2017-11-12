import pandas as pd

import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import wordpunct_tokenize
#import re
from nltk.corpus import stopwords

from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = '/home/collin/stanford-parser-full-2017-06-09/stanford-parser.jar'
path_to_models_jar = '/home/collin/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

stemmer = SnowballStemmer('english')
def stem(w):
    return stemmer.stem(w)

DR_one = ['nsubj','dobj','xsubj','csubj','nmod','iobj']
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
                H = False
                dep_dict = dict(node['deps'])
                #R_4_1
                if 'conj' in dep_dict.keys():
                    conj_index = dep_dict['conj'][0]
                    w1 = stem(node['word'])
                    w2 = stem(dep_list[conj_index]['word'])
                    if node['tag'][:2] == 'JJ' and dep_list[conj_index]['tag'][:2] == 'JJ':
                        if w1 in opinion_list or w2 in opinion_list:
                            dict_add(opinion_dict, w1, node['word'])
                            dict_add(opinion_dict, w2, dep_list[conj_index]['word'])
                        
                index_list = extract_rule(dep_dict)
                i_list = []
                for index in index_list:
                    i_list += index
                    
                if len(i_list) > 0:
                    for index in i_list:
                        #print(index)
                        opinion = stem(dep_list[index]['word'])
                        #print(opinion)
                        if opinion in opinion_list:
                            H = True
                            break
                    if H == True:
                        for index in i_list:
                            word = dep_list[index]
                            #R_1_2
                            w = stem(word['word'])
                            if w in target_list and word['tag'][:2] == 'NN':
                                dict_add(target_dict, w, word['word'])
                            #R_1_1
                            w = stem(node['word'])
                            if w in target_list and node['tag'][:2] == 'NN':
                                dict_add(target_dict, w, node['word'])
                        #R_4_2
                        for index in index_list:
                            if len(index) == 1:
                                continue

                            for i in index:
                                w = stem(dep_list[i]['word'])
                                if w in opinion_list and dep_list[i]['tag'][:2] == 'JJ':
                                    dict_add(opinion_dict, w, dep_list[i]['word'])
    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
            H = False
            
            dep_dict = dict(node['deps'])
            #R_3_1
            if 'conj' in dep_dict.keys():
                conj_index = dep_dict['conj'][0]
                w1 = stem(node['word'])
                w2 = stem(dep_list[conj_index]['word'])
                if node['tag'][:2] == 'NN' and dep_list[conj_index]['tag'][:2] =='NN':
                    if w1 in target_list or w2 in target_list:
                        dict_add(target_dict, w1, node['word'])
                        dict_add(target_dict, w2, dep_list[conj_index]['word'])
            
            index_list = extract_rule(dep_dict)
            i_list = []
            for index in index_list:
                i_list += index
                
            if len(i_list) > 0:
                target = stem(node['word'])
                #print(target)
                if target in target_list:
                    #print(target)
                    H = True
                
                if H == True:
                    for index in i_list:
                        word = dep_list[index]
                        w = stem(word['word'])
                        #R_2_1
                        if w in opinion_list and word['tag'][:2] == 'JJ':
                            dict_add(opinion_dict, w, word['word'])
                            
            H = False
            if len(i_list) > 0:
                for index in i_list:
                    #print(index)
                    target = stem(dep_list[index]['word'])
                    #print(target)
                    if target in target_list:
                        H = True
                        break
                #R_2_2
                if H == True:
                    for index in i_list:
                        opinion = dep_list[index]
                        w =stem(opinion['word'])
                        if w in opinion_list and opinion['tag'][:2] == 'JJ':
                            dict_add(opinion_dict, w, opinion['word']) 
                        
                #R_3_2
                for index in index_list:
                    if len(index) == 1:
                        continue
                    for i in index:
                        w = stem(dep_list[i]['word'])
                        if w in target_list and dep_list[i]['tag'][:2] == 'NN':
                            dict_add(target_dict, w, dep_list[i]['word'])
    for key in target_dict.keys():
        target_dict[key] = list(set(target_dict[key]))
    for key in opinion_dict.keys():
        opinion_dict[key] = list(set(opinion_dict[key]))

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

f1 = open('opinion_list.txt','r')
lines = f1.readlines()
opinion_list =[line.split("\n")[0] for line in lines]

f2 = open('target_list.txt','r')
lines = f2.readlines()
target_list = [line.split("\n")[0] for line in lines]

print opinion_list
print target_list

sents = pd.read_csv('data.csv', index_col = 0)
sents = sents['comment']
#print(sents.head())
print len(sents.index.values)

#opinion_size = len(opinion_list)
#target_size = len(target_list)

sents = sents.values
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
df.to_csv('transactions.csv')
