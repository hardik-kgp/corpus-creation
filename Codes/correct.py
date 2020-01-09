# import the necessary libraries 
import nltk 
import re
from nltk.tokenize import word_tokenize 
from collections import Counter
import pickle 
import os

# Case folding
def text_lowercase(text): 
	return text.lower() 

# Remove special characters 
def remove_nonalphanum(text): 
	result = re.sub(" \d+", " ", text)
	#result = re.sub(r'[^\d\w\s\n\t]+', ' ', text) 
	return result 

# Remove stopwords
def remove_stopwords(text,stop_words):  
	word_tokens = word_tokenize(text) 
	filtered_text = [word for word in word_tokens if word not in stop_words] 
	return ' '.join(filtered_text)

db = open('stopwords.pckl','rb')
stop_words = pickle.load(db)
word_count = Counter()


for subdir, dirs, files in os.walk('../Corpus/filtered'):
	for file in files:
		#print os.path.join(subdir, file)
		filepath = subdir + os.sep + file
		if filepath.endswith(".txt"):
			print (filepath)
			with open(filepath, 'r') as f:
				text = '\n'.join(f.readlines())

			text = text_lowercase(text)
			text = remove_nonalphanum(text)
			text = remove_stopwords(text,stop_words)
			with open(filepath,'w') as f:
				f.write(text)
			print(text)
			#col = Counter(text.split())
			#word_count += col


#with open('word_count.pckl', 'wb') as f:
#	pickle.dump(word_count, f)			
#print(word_count)


