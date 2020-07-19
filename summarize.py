from nltk.corpus import stopwords
from nltk.cluster.util import cosine_distance
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import spacy

def reed(article):
    article = article.split(". ")
    s=len(article)
    sentences = []
    for sentence in article:
        #print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z0-9]", " ").split(" "))
    sentences.pop() 
    #print("\n\n",sentences)
    return s,sentences

def sentence_sim(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
    all_words = list(set(sent1 + sent2))
    #print(all_words)
    vect1 = [0] * len(all_words)
    vect2 = [0] * len(all_words)
    for w in sent1:
        if w in stopwords:
            continue
        vect1[all_words.index(w)] += 1
    for w in sent2:
        if w in stopwords:
            continue
        vect2[all_words.index(w)] += 1
 
    return 1 - cosine_distance(vect1, vect2)

def sim_mat(sentences, stop_words):
    sim_mat = np.zeros((len(sentences), len(sentences)))
    for id1 in range(len(sentences)):
        for id2 in range(len(sentences)):
            if id1 == id2:
                continue 
            sim_mat[id1][id2] = sentence_sim(sentences[id1], sentences[id2], stop_words)
    return sim_mat

def test3_group(sim_mats):
  final_list=[]
  for id1 in range(len(sim_mats)):
    for i in final_list:
      if id1 in i:
        index=final_list.index(i)
        break
    for id2 in range(len(sim_mats)):
       if sim_mats[id1][id2]>0.1:
         pass

def test2_group(sim_mats):
  finnal_list=[]
  lis=[0]*len(sim_mats)
  for id1 in range(len(sim_mats)):
    if lis[id1]==0:
      lis[id1]=1
      finnal_list.append([id1])
      index=-1
    else:
      for i in finnal_list:
        if id1 in i:
          index=finnal_list.index(i)
    for id2 in range(len(sim_mats)):
      if lis[id1]==0:
        if sim_mats[id1][id2] > 0.09:
          finnal_list[index].append(id2)
        elif sim_mats[id1][id2] == 0:
          continue
        else:
          finnal_list.append([id2])
  return finnal_list

def test_group(sim_mats):
  final_list=[]
  finnal_list=[]
  for id1 in range(len(sim_mats)):
    flag=0
    index=-1
    for i in final_list:
      if id1 in i:
        flag=1
        index=final_list.index(i)
        break
    if flag==0:
      final_list.append([id1])      
    for id2 in range(len(sim_mats)):
      #print(sim_mats[id1][id2])
      if sim_mats[id1][id2]>0.1:
        '''flag2=0
        for i in final_list:
          if id2 in i:
            flag2=1
            break
        if flag2==0:'''
        final_list[index].append(id2)
      elif sim_mats[id1][id2]==0:
        continue
      else :
        flag2=0
        for i in final_list:
          if id2 in i:
            flag2=1
            break
        if flag2==0:
          final_list.append([id2])
  for i in final_list:
    finnal_list.append(list(set(i)))
  return final_list

def sum_re(sim_mats,sentences,top_n):

    group=test1_group(sim_mats)
    #print(group)
    return None

def call(para):
    nlp = spacy.load("en_core_web_sm") 
    stop_words = stopwords.words('english')
    summarise_text = []
    summarize_text = []
    s,sentences =  reed(para)
   
    top_n=round(s*0.2)
    i=0
    test=" ".join(sentences[0])
    test=nlp(test)
    test2=[pro.pos_ for pro in test]
    #print(test2)
    if ('PROPN' in test2 or 'NOUN' in test2):
      u=sentences.pop(0)
      #print(u)
      summarize_text.append(" ".join(u))
    #print("\n\n",s,"\t",top_n)
    sim_mats= sim_mat(sentences, stop_words)
    #print(sim_mats)
    sim_graph = nx.from_numpy_array(sim_mats)
    #nx.draw(sim_graph,with_labels = True)
    #plt.show()
    scores = nx.pagerank(sim_graph)
    #print("\n\n",scores)
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
    #print("After sorted ", ranked_sentence)    
    for i in range(top_n):
      summarise_text.append(" ".join(ranked_sentence[i][1]))
    for j in sentences:
      if " ".join(j) in summarise_text:
        summarize_text.append(" ".join(j))
    #print("\n\n\n\n Summarised Text: \n", ". ".join(summarize_text))
    #sum_re(sim_mats,sentences,top_n)
    w=". ".join(summarize_text)
    return w