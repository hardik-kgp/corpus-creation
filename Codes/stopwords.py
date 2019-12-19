import pickle
with open('stopwords.txt', 'r+') as f:
    stopwords = [line.strip() for line in f]
stopwords = set(stopwords)

with open('stopwords.pckl', 'wb') as f:
	pickle.dump(stopwords, f)
