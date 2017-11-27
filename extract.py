import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import wordpunct_tokenize
import re
from nltk.corpus import stopwords
import pandas as pd

from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = '/Users/collin/stanford/stanford-parser-full-2017-06-09/stanford-parser.jar'
path_to_models_jar = '/Users/collin/stanford/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

stemmer = SnowballStemmer('english')
def stem(w):
    return stemmer.stem(w)

DR_one = ['nsubj','dobj','xsubj','csubj','nmod','iobj']
DR_two = ['amod']
#DR_two = ['nsubj','dobj','xsubj','csubj','nsubjpass','nmod','iobj']
DR_three = ['conj']
DR = DR_one + DR_three

opinion_list = ['good','bad','busy','fine','fast','quick','slow']
opinion_list = [stem(item) for item in opinion_list]
print(opinion_list)
target_list = []

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

def extract_target_opinion(s):
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
                    if w1 in opinion_list and dep_list[conj_index]['tag'][:2] == 'JJ' and w2 not in opinion_list:
                        opinion_list.append(w2)
                    if w1 not in opinion_list and node['tag'][:2] == 'JJ' and w2 in opinion_list:
                         opinion_list.append(w1)
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
                            if word['tag'][:2] =='NN' and w not in target_list:
                                target_list.append(w)
                            #R_1_1
                            w = stem(node['word'])
                            if node['tag'][:2] == 'NN' and w not in target_list:
                                target_list.append(w)
                        #R_4_2
                        for index in index_list:
                            if len(index) == 1:
                                continue
                            
                            flag = False
                            for i in index:
                                if dep_list[i]['word'] in opinion_list:
                                    flag = True
                            if flag == True:
                                for i in index:
                                    w = stem(dep_list[i]['word'])
                                    if dep_list[i]['tag'][:2] == 'JJ' and w not in opinion_list:
                                        opinion_list.append(w)
    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
            H = False
            
            dep_dict = dict(node['deps'])
            #R_3_1
            if 'conj' in dep_dict.keys():
                conj_index = dep_dict['conj'][0]
                w1 = stem(node['word'])
                w2 = stem(dep_list[conj_index]['word'])
                if w1 in target_list and dep_list[conj_index]['tag'][:2] == 'NN' and w2 not in target_list:
                    target_list.append(w2)
                if w1 not in target_list and node['tag'][:2] == 'NN' and w2 in target_list:
                     target_list.append(w1)
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
                        if w not in opinion_list and word['tag'][:2] == 'JJ':
                            opinion_list.append(w)
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
                        if w not in opinion_list and opinion['tag'][:2] == 'JJ':
                            opinion_list.append(w)    
                        
                #R_3_2
                for index in index_list:
                    if len(index) == 1:
                        continue
                        
                    flag = False
                    for i in index:
                        w = stem(dep_list[i]['word'])
                        if w in target_list:
                            flag = True
                    if flag == True:
                        for i in index:
                            w = stem(dep_list[i]['word'])
                            if dep_list[i]['tag'][:2] == 'NN' and w not in target_list:
                                target_list.append(w)

def parse_comment(sents):
    sent_list = sent_tokenize(sents)
    for sent in sent_list:
        extract_target_opinion(sent)

sents = pd.read_csv('data.csv', index_col = 0)
sents = sents['comment']#.iloc[:2]
#print(sents.head())
print len(sents.index.values)

opinion_size = len(opinion_list)
target_size = len(target_list)

sents.apply(parse_comment)
count = 1
print(count)
while(opinion_size != len(opinion_list) or target_size != len(target_list)):
    opinion_size = len(opinion_list)
    target_size = len(target_list)
    sents.apply(parse_comment)
    count += 1
    print(count)

f1 = open('opinion_list_1.txt','w')
f2 = open('target_list_1.txt','w')
for opinion in opinion_list:
    f1.write(opinion+'\n')
f1.close()
for target in target_list:
    f2.write(target+'\n')
f2.close()

#print(opinion_list)
#print(target_list)
