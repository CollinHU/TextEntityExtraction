from extract import extract_target_opinion
import pandas as pd

def parse_comment(sents):
    sent_list = sent_tokenize(sents)
    for sent in sent_list:
        extract_target_opinion(sent)

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
f1 = open('opinion_list.txt','w')
f2 = open('target_list.txt','w')
for opinion in opinion_list:
    f1.write(opinion+'\n')
f1.close()
for target in target_list:
    f2.write(target+'\n')
f2.close()
print(opinion_list)
print(target_list)
