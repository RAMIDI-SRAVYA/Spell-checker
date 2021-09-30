# Spell checker for organizations 
### _custom spell checker_

The spell check feature checks for misspellings in the text given by user and corrects all the misspelled words in the user query. Spell check has the following two modules.
- Corpus dictionary 
- Spell checker

## Features

- #### Corpus dictionary
    Corpus dictionary is a text file that contains all the distinct words obtained by tokenizing the raw corpus, detected abbreviations, generated synonyms, phrases and one-word descriptions. The process in building the corpus dictionary is as follows.
1.	Tokenization of the data present in raw corpus, detected abbreviations, generated synonyms, phrases and one-word descriptions.
2.	Adding only non-numeric data to the corpus dictionary file.
3.	Words containing hyphen are added such that even the words obtained after removing hyphen also exists in the corpus dictionary file.
4.	These words are stored as a pickle file and text file.
5.	The purpose of storing them in a text file is that only ANSI encoded text file format is supported by the “enchant” library that is used to correct misspelled words.

- #### Spell checker
    The spell checker has both standard spell checker and custom spell checker integrated.
1.	The standard spell checker corrects all the misspelled words according to the US English dictionary.
2.	The custom spell checker corrects the misspelled abbreviations, corpus words, etc. according to the corpus dictionary.
3.	Each word in the user query is checked if it is wrongly spelled.
4.	If it is wrongly spelled, then the word is corrected according to the suggestions of the corpus dictionary.
5.	And if there are no suggestions from the corpus dictionary, then the wrongly spelled word is corrected according to the suggestions of the standard dictionary.
6.	Thus, the user query is returned after necessary corrections.

## Prerequistes to run the code
The code requires the following installatins to run.
- pip install nltk
- pip install pickle
- pip install pandas
- pip install pyenchant
- pip install datetime
- pip install csv-reader
