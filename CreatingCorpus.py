# Importing packages
import re
import unicodedata
import numpy as np
import pandas as pd
import os
import nltk
import sys
from sklearn.model_selection import train_test_split

# Defining some helper functions
# Whitespace padding punctuation
def whitespace_punct(x):
	# Padding punctuation
	x = re.sub(r'([\'.,!?;()"])', r' \1 ', x).strip()
	x = re.sub(r'\s{2,}',' ',x).strip()
	return x

def clean_text(x):
	# Replacing special characters with whitespace
	x = re.sub(r'[\n\t\r]',' ',x)
	# Replacing weird characters
	x = x.replace('”','"').replace('“','"').replace('’',"'").replace('‘',"'").replace('_',' ').replace('-',' ').replace('_',' ')
	# Replacing multiple whitespaces
	x = re.sub(r'\s{2,}',' ',x)
	# Sending everthing to lowercase
	x = x.lower()
	# Keeping only alphanumeric and certain punctuation
	#x = re.sub(r'[^a-z0-9.,\'";:!?]','',x)
	# Sentence Tokenization
	tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
	abbrevs = set(['dr','mr','mrs','prof','ms'])
	tokenizer._params.abbrev_types.update(abbrevs)
	x = tokenizer.tokenize(x)
	# Cleaning whitespaces
	x = [whitespace_punct(i) for i in x]
	# Limiting the sentence size to 30 words
	x = [' '.join(i.split()[0:30]) for i in x]
	# We now need to get rid of empty sentences
	x = [i for i in x if i]
	# Addign start and stop tokens
	x = ['<start> '+i+' <end>' for i in x]
	return x

# Importing the list of texts from Gutenberg
files = os.listdir('C:/Users/Jacob/Desktop/Paraphrase/Gutenberg/txt/')

# Creating the list of authors
authors = [x.split('___')[0] for x in files]

# Creating our list of data frames to concat later on
df_list = []

# Going through each document and tokenizing sentences
for i in range(len(files)):
	# Grabbing the text
	text = open('C:/Users/Jacob/Desktop/Paraphrase/Gutenberg/txt/'+files[i], 'r', encoding='utf8').read()
	# Cleaning the text with our function
	text = clean_text(text)
	# Preparing current, post, and prev sentences for skip-thoughts
	current = text[1:-1]
	prev = text[:-2]
	post = text[2:]
	# Declaring our dict for later
	text_dict = {'author':authors[i],
				 'current':current,
				 'previous':prev,
				 'next':post}
	# Appending to our dataframe
	df_list.append(pd.DataFrame(text_dict,index=range(len(text)-2)))
	# Printing iteration
	sys.stdout.write('\rCompleted '+str(i)+'/'+str(len(files)))
	sys.stdout.flush()

# Concatenating our data
df = pd.concat(df_list, axis=0)
print('\nFinal Data Shape:',df.shape)

# Writing the dataframe
df.to_csv('TextCorpus.csv',encoding='utf8',index=False)

# Saving a sample
df.sample(1000000).to_csv('TextCorpusSample.csv',encoding='utf8',index=False)