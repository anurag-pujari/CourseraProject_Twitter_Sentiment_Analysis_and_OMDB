#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 18 14:04:11 2020

@author: anurag
"""
import pandas as pd
punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@', '-']
                     
def strip_punctuation(word):
    word = word
    for chars in word:
        if chars in punctuation_chars:
            word = word.replace(chars,"")
    return word

positive_words = []
with open("positive-words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            positive_words.append(lin.strip())


negative_words = []
with open("negative-words.txt") as pos_f:
    for lin in pos_f:
        if lin[0] != ';' and lin[0] != '\n':
            negative_words.append(lin.strip())


def get_pos(sentence):
    count = 0;
    sentence = strip_punctuation(sentence)
    listOfWords = sentence.split()
    for words in listOfWords:
        for pos_words in positive_words:
            if words == pos_words:
                count+= 1
    return count

def get_neg(sentence):
    count = 0
    sentence = strip_punctuation(sentence)
    listOfWords = sentence.split()
    for words in listOfWords:
        for neg_words in negative_words:
            if words == neg_words:
                count+= 1
    return count
              
data = pd.read_csv("project_twitter_data.csv")
retweets = data["retweet_count"]
retweets = retweets.tolist()
replies = data["reply_count"]
replies = replies.tolist()
texts = data["tweet_text"]
neg_counts = []  
pos_counts = []

for text in texts:
    counts_pos = get_pos(text)
    counts_neg = get_neg(text)
    pos_counts.append(counts_pos)
    neg_counts.append(counts_neg)  

total  = [neg_counts[values] + pos_counts[values] for values in range(len(neg_counts))]
df = pd.DataFrame({"retweets":retweets,"replies":replies,"neg_counts":neg_counts,"pos_counts":pos_counts,"Net_score":total})
df.to_csv("resulting_data.csv")
