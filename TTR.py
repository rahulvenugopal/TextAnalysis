#!/usr/bin/env python
'''
Rewrote to automate file selection and extract some parameters to a neat dataframe

Application to calculate the Type-Token Ratio from a speech sample.

Copyright (C) 2013 Steven C. Howell

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Please report any issues on-line at:
https://github.com/StevenCHowell/type_token_ratio/issues

author @ Rahul Venugopal on 2nd February 2024
'''

#%% Import libraries

import collections
import string
import pandas as pd
import os

#%% Create a master output df


# Initialise empty lists for columns
TokenRatio = []
TotalWords = []
UWords = []
fnames = []

for file in os.listdir():
    if file.endswith('.txt'):
        fnames.append(file)

#%% Looping through files
for file in fnames:
    
    # Open and read the text file
    file = open(file,'r')
    data = file.readlines()    
    
    words = []
    
    # gather all the words
    for line in data:
        new_words = line.split()
        words += [word.lower() for word in new_words]
    
    n_words = len(words)
    
    # remove all punctuations
    for i in range(n_words):
        for c in string.punctuation:
            words[i] = words[i].replace(c,'')
    
    # remove empty words
    words = list(filter(None, words))
    
    # count each word
    word_count = collections.Counter(words)
    
    # get the sorted list of unique words
    unique_words = list(word_count.keys())
    unique_words.sort()
    
    n_unique = len(unique_words)
    ttr = len(word_count)/float(len(words))
    
    # Add to main list
    TokenRatio.append(ttr)
    TotalWords.append(len(word_count))
    UWords.append(n_unique)
    
#%% Spit out the dataframe as a csv
dict = {'filename': fnames, 'TotalWords': TotalWords, 'UniqueWords': UWords, 'TypeTokenRatio': TokenRatio} 
    
df = pd.DataFrame(dict)

df.to_csv('Type token ratio output.csv', sep=',', encoding='utf-8', index=False)
