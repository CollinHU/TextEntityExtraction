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


stemmer = SnowballStemmer('english')
def stem(w):
    return stemmer.stem(w)

DR_one = ['nsubj','dobj','xsubj','csubj','nmod','iobj','xcomp']
DR_two = ['amod']
#DR_two = ['nsubj','dobj','xsubj','csubj','nsubjpass','nmod','iobj']
DR_three = ['conj']
DR = DR_one + DR_three

#opinion_list = ['helpful','practical','sophisticated','good','bad','busy','fine','fast','quick','slow','easy']
#opinion_list = [stem(item) for item in opinion_list]

data_file = "course_meQ0ic9uEeWu4RLrx6VBYw"
opinion_file = "opinion_list.txt"
target_file = "../result/{}_target_list.txt".format(data_file)
data_file = "../data/course/" + data_file + ".csv"

f1 = open(opinion_file,'r')
lines = f1.readlines()
opinion_list =[line.split("\n")[0] for line in lines]

#print(opinion_list)
target_list = []
def extract_rule(dep_dic):
    value_list = []
    one_list = []
    two_list = []
    for key,value in dep_dic.items():
        if key in DR_one:
            one_list += value
        elif key in DR_two:
            two_list += value
    value_list.append(one_list)
    value_list.append(two_list)      
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
                        if node['tag'][:2] == 'NN' and w not in target_list:
                            target_list.append(w)
                        #R_1_2
                        for index in i_list:
                            word = dep_list[index]
                            w = stem(word['word'])
                            if word['tag'][:2] =='NN' and w not in target_list:
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
                    #R_2_1
                    w = stem(node['word'])
                    if node['tag'][:2] == 'JJ' and w not in opinion_list:
                        opinion_list.append(w)
                    #R_2_2
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

sents = pd.read_csv(data_file, index_col = 0)
sents['comment'] = sents['comment'].apply(process_sentence)
sents = sents['comment'].values
#print(sents[0])
size = len(sents)
print(size)

opinion_size = len(opinion_list)
target_size = len(target_list)

#sents.apply(parse_comment)
count = 1
print(count)
for i in range(size):
	if (i + 1) % 300 == 0:
		server.stop()
		server.start()
	#print(i)
	parse_comment(sents[i])
print("finish iteration ", count)

server.stop()
while(opinion_size != len(opinion_list) or target_size != len(target_list)):
    try:
        server.start()
        count += 1
        print(count)
        dependency_parser = CoreNLPDependencyParser()
        opinion_size = len(opinion_list)
        target_size = len(target_list)
        for i in range(size):
        	if (i + 1) % 300 == 0:
        		server.stop()
        		server.start()
        	#print(i)
        	parse_comment(sents[i])
        print("finish iteration ", count)
        server.stop()
    except:
        print('something wrong')

f1 = open(opinion_file,'w')
f2 = open(target_file,'w')
for opinion in opinion_list:
    f1.write(opinion+'\n')
f1.close()
for target in target_list:
    f2.write(target+'\n')
f2.close()
server.stop()
#print(opinion_list)
#print(target_list)
