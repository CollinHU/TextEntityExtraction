import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer
from nltk import wordpunct_tokenize
import re
from nltk.corpus import stopwords
import pandas as pd

##2017 12 3 using a different parser to parse sentence
'''
from nltk.parse.stanford import StanfordDependencyParser
path_to_jar = '/home/collin/stanford-parser-full-2017-06-09/stanford-parser.jar'
path_to_models_jar = '/home/collin/stanford-parser-full-2017-06-09/stanford-parser-3.8.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
'''
from nltk.parse.corenlp import CoreNLPServer, CoreNLPDependencyParser
path_to_jar = '/Users/collin/stanford/stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0.jar'
path_to_models_jar = '/Users/collin/stanford/stanford-corenlp-full-2017-06-09/stanford-corenlp-3.8.0-models.jar'
server = CoreNLPServer(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)
server.start()
dependency_parser = CoreNLPDependencyParser()


stemmer = SnowballStemmer('english')

def parse_sent(s):
    s_list = sent_tokenize(s)
    #dependency relation list
    dr_list = []
    for item in s_list:
        result = dependency_parser.raw_parse(item)
        #dependecy graph
        dr_g = next(result)
        dr = list(dr_g.triples())
        #print(dep)
        dr_list.append(dr)

    return dr_list#ne_chunk(pos_tag(s_list))

df = pd.read_csv('data/step2_data.csv',index_col = 0)

df['parsed_sent'] = df['comment'].apply(parse_sent)

df = df[['course_id','comment','parsed_sent']]
df.to_csv('data/parsed_sent.csv')
print('finished')