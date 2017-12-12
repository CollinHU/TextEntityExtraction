import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import wordpunct_tokenize
import re
from nltk.corpus import stopwords
import pandas as pd
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

##file name 
data_file = "Canon_G3.csv"
opinion_file = "opinion_list.txt"
target_file = "{}_extracted_target.txt".format(data_file.split('.')[0])

#############
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

def dict_update(target_dict, new_w, word):
    if new_w in target_dict.keys():
        target_dict[new_w].append(word)
    else:
        target_dict[new_w] = [word]

def extract_target_phase(target_dict, s):
    ##parse the sentence
    result = dependency_parser.raw_parse(s)
    dep = next(result)
    dep_list = dict(sorted(dep.nodes.items()))

    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
            w = stem(node['word'])
            dep_dict = dict(node['deps'])
            if w in target_list and node['tag'][:2] == 'NN' and 'compound' in dep_dict.keys():
                new_w = ''
                word = ''
                for index in dep_dict['compound']:
                    if new_w =='':
                        comp_word = dep_list[index]['word']
                        comp_w = stem(comp_word)
                        new_w = comp_w
                        word = comp_word
                    else:
                        comp_word = dep_list[index]['word']
                        comp_w = stem(comp_word)
                        new_w = new_w + ' ' + comp_w
                        word = word + ' ' + comp_word
                new_w = new_w + ' ' + w
                word = word + ' ' + node['word']
                dict_update(target_dict, new_w, word)
            elif w in target_list and node['tag'][:2] == 'NN' and node['rel'] !='compound':
                dict_update(target_dict, w, node['word'])


def update_target(sents):
    target_d = {}
    sent_list = sent_tokenize(sents)
    for sent in sent_list:
        extract_target_phase(target_d,sent)
    for key in target_d.keys():
        target_d[key] = list(set(target_d[key]))
    return target_d


f1 = open(opinion_file,'r')
lines = f1.readlines()
opinion_list =[line.split("\n")[0] for line in lines]

f2 = open(target_file,'r')
lines = f2.readlines()
target_list = [line.split("\n")[0] for line in lines]

print(opinion_list)
print(target_list)

df = pd.read_csv(data_file,index_col = 0)
df['comment'] = df['comment'].apply(process_sentence)
sents = df['comment'].values

size = len(df)


target_dict = []
for i in range(size):
    #print(i)
    dic = update_target(sents[i])
    target_dict.append(dic)

dict_df = {'comment':list(df['comment']), 'target':target_dict}
new_df = pd.DataFrame(data = dict_df)
new_df.head()
new_df.to_csv('{}_transaction_v3.csv'.format(data_file.split('.')[0]))

server.stop()
print("finish..")
