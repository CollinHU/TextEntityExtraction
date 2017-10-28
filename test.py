
# coding: utf-8

# In[1]:

import nltk
from nltk import sent_tokenize,word_tokenize, pos_tag, ne_chunk
from nltk.stem.snowball import SnowballStemmer


# In[2]:

s1 = "Mark and John are working at Google."
s2 = "Hello. My name is Jacob. You'll be learning NLTK today."
s3 = "Today is Tuesday."
s4 = "Names are interesting."
s_list = [s1, s2, s3, s4]


# In[3]:

stemmer = SnowballStemmer("english", ignore_stopwords=True)
def extract_entity(s):
    return ne_chunk(pos_tag(word_tokenize(s)))


# In[4]:

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
    #print("tree:", tree)
    for subtree in T:
        if type(subtree) == nltk.tree.Tree:
            traverseTree(subtree, num)
        else:
            if judge_subT(subtree[1]) and judge_tree(T):
                #print(T.label())
                #print(subtree[0])
                item = stemmer.stem(subtree[0])
                if item not in s_level_dict.keys():
                    s_level_dict[item]= [num]
                else:
                    s_level_dict[item] += [num]


# In[5]:

tree_list = []
N = len(s_list)
for i in range(N):
    s = sent_tokenize(s_list[i])
    for item in s:
        T = extract_entity(item)
        #print(T)
        traverseTree(T, i)

print(s_level_dict)


# In[6]:

dict = {}
if 'p' not in dict.keys():
    dict['p'] = 1
print(dict)


# In[27]:

from nltk import wordpunct_tokenize
from nltk.corpus import stopwords
from nltk.corpus import words


# In[31]:

print(words.fileids())
print words.words('en')[0:10]


# In[75]:

def calculate_language_ratios(text):
    languages_ratios = {}
    tokens = wordpunct_tokenize(text)
    sen_size = len(tokens)
    #print(sen_size)
    T_words = [word.lower() for word in tokens]
    #for language in words.fileids():
    words_set = set(words.words('en'))
    T_words_set = set(T_words) 
    common_elements = T_words_set.intersection(words_set)
    print len(common_elements)
    print sen_size
    ratio = float(len(common_elements))/sen_size
    return ratio


# In[76]:

text = "Good course. Learned a lot from it. Thanks!"
language = calculate_language_ratios(text)
print(language)


# In[ ]:




# In[ ]:



