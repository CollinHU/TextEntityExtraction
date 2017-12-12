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

def dict_update(target_dict, old_w, new_w, comp_word, word):
    target_dict[old_w].remove(word)
    if new_w in target_dict.keys():
        target_dict[new_w].append(comp_word + ' ' + word)
    else:
        target_dict[new_w] = [comp_word + ' ' + word]

def extract_target_phase(target_dict, s):
    ##parse the sentence
    result = dependency_parser.raw_parse(s)
    dep = next(result)
    dep_list = dict(sorted(dep.nodes.items()))

    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
                H = False
                dep_dict = dict(node['deps'])
                index_list = extract_rule(dep_dict)
                i_list = []
                for index in index_list:
                    i_list += index
                    
                if len(i_list) > 0:
                    if stem(node['word']) in opinion_list:
                        #print(node['word'])
                        H = True
                    for index in i_list:
                        #print(index)
                        opinion = stem(dep_list[index]['word'])
                        #print(opinion)
                        if opinion in opinion_list:
                            H = True
                            break
                    
                    if H == True:
                        #R_1_1
                        w = stem(node['word'])
                        if w in target_list and node['tag'][:2] == 'NN' and 'compound' in node['deps']:
                            comp_index = node['deps']['compound'][0]
                            comp_word = dep_list[comp_index]['word']
                            comp_w = stem(comp_word)
                            old_w = w
                            new_w = comp_w + ' ' + w
                            dict_update(target_dict, old_w, new_w, comp_word, node['word'])
                        #R_1_2
                        for index in i_list:
                            word = dep_list[index]
                            w = stem(word['word'])
                            if w in target_list and word['tag'][:2] == 'NN' and 'compound' in word['deps']:
                                comp_index = word['deps']['compound'][0]
                                comp_word = dep_list[comp_index]['word']
                                comp_w = stem(comp_word)
                                old_w = w
                                new_w = comp_w + ' ' + w
                                dict_update(target_dict, old_w, new_w, comp_word, word['word'])
    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
            dep_dict = dict(node['deps'])
            #R_3_1
            if 'conj' in dep_dict.keys():
                conj_index = dep_dict['conj'][0]
                w1 = stem(node['word'])
                word = dep_list[conj_index]
                w2 = stem(word['word'])
                if node['tag'][:2] == 'NN' and word['tag'][:2] =='NN':
                    if w1 in target_list and 'compound' in node['deps']:
                        comp_index = node['deps']['compound'][0]
                        comp_word = dep_list[comp_index]['word']
                        comp_w = stem(comp_word)
                        old_w = w1
                        new_w = comp_w + ' ' + w1
                        dict_update(target_dict, old_w, new_w, comp_word, node['word'])
                    if w2 in target_list and 'compound' in word['deps']:
                        comp_index = word['deps']['compound'][0]
                        comp_word = dep_list[comp_index]['word']
                        comp_w = stem(comp_word)
                        old_w = w2
                        new_w = comp_w + ' ' + w2
                        dict_update(target_dict, old_w, new_w, comp_word, word['word'])
            index_list = extract_rule(dep_dict)
            i_list = []
            for index in index_list:
                i_list += index
            
            if len(i_list) > 0:
                target = stem(node['word'])
                if target in target_list:
                    H = True
                for index in i_list:
                        #print(index)
                        target = stem(dep_list[index]['word'])
                        #print(opinion)
                        if target in target_list:
                            H = True
                            break
            if H == True:
                #R_3_2
                if len(i_list) > 0:
                    for index in index_list:
                        if len(index) == 1:
                            continue
                        for i in index:
                            word = dep_list[i]
                            w = stem(word['word'])
                            if w in target_list and word['tag'][:2] == 'NN' and 'compound' in word['deps']:
                                comp_index = word['deps']['compound'][0]
                                comp_word = dep_list[comp_index]['word']
                                comp_w = stem(comp_word)
                                old_w = w
                                new_w = comp_w + ' ' + w
                                dict_update(target_dict, old_w, new_w, comp_word, word['word'])



def update_target(sents, target):
    target_d = eval(target)
    if len(target_d) == 0:
        return target_d
    sent_list = sent_tokenize(sents)
    for sent in sent_list:
        extract_target_phase(target_d,sent)
    for key in target_d.keys():
        target_d[key] = list(set(target_d[key]))
    return target_d


f1 = open('opinion_list_1.txt','r')
lines = f1.readlines()
opinion_list =[line.split("\n")[0] for line in lines]

f2 = open('target_list_1.txt','r')
lines = f2.readlines()
target_list = [line.split("\n")[0] for line in lines]

print(opinion_list)
print(target_list)

df = pd.read_csv('data.csv',index_col = 0)
df_n = pd.read_csv('transactions.csv',index_col = 0)
df['target'] = df_n['target']

comments = df['comment'].values
targets = df['target'].values
print(len(targets))

size = len(comments)
target_dict = []
for i in range(size):
    print(i)
    dic = update_target(comments[i],targets[i])
    new_dic = {}
    for key in dic.keys():
        if len(dic[key]) != 0:
            new_dic[key] = dic[key]
    target_dict.append(new_dic)
dict_df = {'comment':list(df['comment']), 'target':target_dict}
new_df = pd.DataFrame(data = dict_df)
new_df.head()
new_df.to_csv('new_transaction.csv')
print("finish..")
