import csv
from itertools import islice
from sklearn.feature_extraction.text import CountVectorizer

N = 1000

bodies = None
word_counts = {}

with open('data/questions-bodies-unedited-2015.csv') as bodies_file:
        bodies = csv.DictReader(bodies_file)
        # bodies = islice(bodies, N)
        bodies = [row['body'] for row in bodies]

# make a CountVectorizer-style tokenizer
tokenizer = CountVectorizer().build_analyzer()

for body in bodies:
    for word in tokenizer(body):
        word_counts[word] = word_counts.get(word, 0) + 1

#print(word_counts)

hapaxes = []

for word in word_counts:
	if word_counts[word] == 1:
	    hapaxes.append(word)

hapaxes_string = '\n'.join(hapaxes)

with open('data/hapaxes.txt', 'w') as hapaxes_file:
    hapaxes_file.write(hapaxes_string)

#print(hapaxes)