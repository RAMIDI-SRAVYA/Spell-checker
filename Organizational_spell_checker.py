#!/usr/bin/env python
# coding: utf-8

# In[8]:


import enchant
import nltk
from datetime import datetime
from csv import reader
import pandas as pd
import pickle
import os
import codecs


# In[9]:


def create_pickle(file, data):
    open_file = open(file, 'wb')
    pickle.dump(data, open_file)
    open_file.close()
    
def build_corpus_dictionary(corpus_file):   
    if os.path.exists("corpus.txt"):
        os.remove("corpus.txt")

    #text file that stores the distinct words
    corpus_dict = open("corpus.txt", "a", encoding = 'cp1252')
    words_set = set()

    #this reads the corpus csv file
    with open(corpus_file, 'r', encoding = "utf8") as read_obj:
        csv_reader = reader(read_obj)
        for row in csv_reader:
            for col in row:
                tokenizer = nltk.RegexpTokenizer(r"\w+")
                words_list = tokenizer.tokenize(col)
                for word in words_list:
                    if word.isnumeric() == False:
                        words_set.add(word)
                        words_set.add(word.lower())

    #this reads the generated synonyms
    syn = pd.read_pickle('word_synonymlist.pickle')
    for items in syn:
        if items.isnumeric() == False: 
            words_set.add(items)
            for word in syn[items]:
                if word.isnumeric() == False: 
                    #if the word contains space(' ')
                    j = 0
                    for i in range(0, len(word)):
                        if word[i] == ' ':
                            if word[j:i].isnumeric() == False:
                                words_set.add(word[j:i])
                                j = i + 1
                    words_set.add(word[j:])

    #this reads the detected abbreviaions
    abb = pd.read_pickle('abbreviations.pickle')
    for item in abb:
        for word in abb[item]:
            if word.isnumeric() == False:
                words_set.add(word)
                words_set.add(word.lower())
                #if the word contains hyphen(-)
                for i in range(0, len(word)):
                    if word[i] == '-':
                        if word[0:i].isnumeric() == False:
                            words_set.add(word[0:i])
                            words_set.add(word[0:i].lower())
                        if word[i+1:].isnumeric() == False:    
                            words_set.add(word[i+1:])
                            words_set.add(word[i+1:].lower())
            if abb[item][word].isnumeric() == False:
                words_set.add(abb[item][word])
                words_set.add(abb[item][word].lower())

    #this reads the detected phrases
    di = pd.read_pickle('phrases.pickle')
    for i in di:
        if i.isnumeric() == False:
            words_set.add(i)
            words_set.add(i.lower())

        for word in di[i]:
            if word.isnumeric() == False:  
                #if the word contains hyphen
                if '-' in word:
                    words_set.add(word)
                    words_set.add(word.lower())   
                #if the word contains space, underscore, hyphen
                j = 0
                for i in range(0, len(word)):
                    if word[i] == ' ' or word[i] == '_' or word[i] == '-':
                        if word[j:i].isnumeric() == False:
                            words_set.add(word[j:i])
                            words_set.add(word[j:i].lower())
                            j = i + 1
                words_set.add(word[j:])
                words_set.add(word[j:].lower())

    #this reads the one word descriptions
    with open('one_word_descriptions.pickle', 'rb') as read_obj:
        pkl_reader = pickle.load(read_obj)
        for items in pkl_reader.items():
            tokenizer = nltk.RegexpTokenizer(r"\w+")
            words_list = tokenizer.tokenize(str(items))
            for word in words_list:
                if word.isnumeric() == False:
                    words_set.add(word)
                    words_set.add(word.lower())


    create_pickle("words_set.pickle", list(words_set))

    for word in words_set:
        try:
            word = word.encode("cp1252").decode("cp1252")
            corpus_dict.write(word)
            corpus_dict.write("\n")
        except:
            pass

    corpus_dict.write('fullform')
    corpus_dict.write("\n")
    corpus_dict.close()
    
corpus_file = "QA_corpus.csv"
start_time = datetime.now()       
build_corpus_dictionary(corpus_file)
end_time = datetime.now()
print("Corpus dictionary created (in minutes):", (end_time-start_time).total_seconds()/60)


# In[10]:


def spell_check(user_input): 
    tokenizer = nltk.RegexpTokenizer(r"\w+")
    words_list = tokenizer.tokenize(user_input)
    
    for word in words_list:
        #check if the word exists in the dictionary
        if word not in corpus_dic:
            if word.isnumeric() == False:
                if standard_dict.check(word) == False:
                    #get suggestions for the input word
                    suggestions = corpus_dict.suggest(word)
                    if(len(suggestions) != 0):
                        user_input = user_input.replace(word, suggestions[0])
                    else:
                        user_input = user_input.replace(word, standard_dict.suggest(word)[0])

    return user_input

corpus_dict = enchant.PyPWL("corpus.txt")
standard_dict = enchant.Dict("en_US")
corpus_dic = pd.read_pickle("words_set.pickle")
user_input = input("Enter the wrongly spelt word: ")
print("The corrected word is: " + spell_check(user_input))


# In[ ]:





# In[ ]:




