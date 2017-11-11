DR_one = ['nsubj','dobj','xsubj','csubj','nmod','iobj']
DR_two = ['amod']
#DR_two = ['nsubj','dobj','xsubj','csubj','nsubjpass','nmod','iobj']
DR_three = ['conj']
DR = DR_one + DR_three

opinion_list = ['good','bad','busy','fine','fast','quick','slow']
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
                    if node['word'] in opinion_list and dep_list[conj_index]['word'] not in opinion_list:
                        opinion_list.append(dep_list[conj_index]['word'])
                    if node['word'] not in opinion_list and dep_list[conj_index]['word'] in opinion_list:
                         opinion_list.append(node['word'])
                index_list = extract_rule(dep_dict)
                i_list = []
                for index in index_list:
                    i_list += index
                    
                if len(i_list) > 0:
                    for index in i_list:
                        #print(index)
                        opinion = dep_list[index]['word']
                        #print(opinion)
                        if opinion in opinion_list:
                            H = True
                            break
                    if H == True:
                        for index in i_list:
                            word = dep_list[index]
                            #R_1_2
                            if word['tag'][:2] =='NN' and word['word'] not in target_list:
                                target_list.append(word['word'])
                            #R_1_1
                            if node['tag'][:2] == 'NN' and node['word'] not in target_list:
                                target_list.append(node['word'])
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
                                    if dep_list[i]['tag'][:2] == 'JJ' and dep_list[i]['word'] not in opinion_list:
                                        opinion_list.append(dep_list[i]['word'])
    for _, node in sorted(dep.nodes.items()):
         if node['word'] is not None:
            H = False
            
            dep_dict = dict(node['deps'])
            #R_3_1
            if 'conj' in dep_dict.keys():
                conj_index = dep_dict['conj'][0]
                if node['word'] in target_list and dep_list[conj_index]['word'] not in target_list:
                    target_list.append(dep_list[conj_index]['word'])
                if node['word'] not in target_list and dep_list[conj_index]['word'] in target_list:
                     target_list.append(node['word'])
            index_list = extract_rule(dep_dict)
            i_list = []
            for index in index_list:
                i_list += index
                
            if len(i_list) > 0:
                target = node['word']
                #print(target)
                if target in target_list:
                    #print(target)
                    H = True
                
                if H == True:
                    for index in i_list:
                        word = dep_list[index]
                        #R_2_1
                        if word['word'] not in opinion_list and word['tag'][:2] == 'JJ':
                            opinion_list.append(word['word'])
            H = False
            if len(i_list) > 0:
                for index in i_list:
                    #print(index)
                    target = dep_list[index]['word']
                    #print(target)
                    if target in target_list:
                        H = True
                        break
                #R_2_2
                if H == True:
                    for index in i_list:
                        opinion = dep_list[index]
                        if opinion['word'] not in opinion_list and opinion['tag'][:2] == 'JJ':
                            opinion_list.append(opinion['word'])    
                        
                #R_3_2
                for index in index_list:
                    if len(index) == 1:
                        continue
                        
                    flag = False
                    for i in index:
                        if dep_list[i]['word'] in target_list:
                            flag = True
                    if flag == True:
                        for i in index:
                            if dep_list[i]['tag'][:2] == 'NN' and dep_list[i]['word'] not in target_list:
                                target_list.append(dep_list[i]['word'])