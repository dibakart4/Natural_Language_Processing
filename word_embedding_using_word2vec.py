# -*- coding: utf-8 -*-
"""Word_Embedding_using_word2Vec.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Q1k5uta4xrLVmkNSCHD8EIopUcDKEe8u
"""

#Import Libraries
import pandas as pd
import numpy as np
import string
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
nltk.download('stopwords')

from google.colab import files
#Upload IMDB_Dataset.csv file from local system to remote colab location
files.upload()

#Create dataframe and store the data from IMDB_Dataset.csv
data = pd.DataFrame()
data = pd.read_csv('IMDB_Dataset.csv', encoding='utf-8')
data.head()

#create empty list
review_data_list = list()

indv_lines = data['review'].values.tolist()
for line in indv_lines:

	#create word tokens as well as remove puntuation in one go
	rem_tok_punc = RegexpTokenizer(r'\w+')

	tokens = rem_tok_punc.tokenize(line)


	#convert the words to lower case
	words = [w.lower() for w in tokens]

	#Invoke all the english stopwords
	stop_word_list = set(stopwords.words('english'))

	#Remove stop words
	words = [w for w in words if not w in stop_word_list]

	#Append words in the review_data_list list.
	review_data_list.append(words)
len(review_data_list)

#Train a Word2Vec model using Gensim
import gensim
Embedding_Dim = 100
#train word2vec model
model = gensim.models.Word2Vec(sentences = review_data_list, size = Embedding_Dim, workers = 4, min_count = 1)
#Vocabulary size
words = list(model.wv.vocab)
print('Here is the Vocabulary Size.. %d' % len(words))

#Finding similar words
model.wv.most_similar('amazing')

model.wv.most_similar('awful')

#Performing some mathematics on word vectors queen + man - woman = ?
model.wv.most_similar_cosmul(positive=['queen','man'], negative=['woman'])

#Finding the odd word out from the list of words given
print(model.wv.doesnt_match("man woman car".split()))

# Importing bokeh libraries for showing how words of similar context are grouped together
import bokeh.plotting as bp
from bokeh.models import HoverTool, BoxSelectTool
from bokeh.plotting import figure, show, output_notebook

#Defining the chart
output_notebook()
plot_chart = bp.figure(plot_width=700, plot_height=600, title="A map/plot of 5000 word vectors",
    tools="pan,wheel_zoom,box_zoom,reset,hover,previewsave",
    x_axis_type=None, y_axis_type=None, min_border=1)

#Extracting the list of word vectors, limiting to 5000, each is of 200 dimensions
word_vectors = [model[w] for w in list(model.wv.vocab.keys())[:5000]]

# Reducing dimensionality by converting the vectors to 2d vectors
from sklearn.manifold import TSNE
tsne_model = TSNE(n_components=2, verbose=1, random_state=0)
tsne_w2v = tsne_model.fit_transform(word_vectors)

# Storing data in a dataframe
tsne_df = pd.DataFrame(tsne_w2v, columns=['x', 'y'])
tsne_df['words'] = list(model.wv.vocab.keys())[:5000]

# Corresponding word appears when you hover on the data point.
plot_chart.scatter(x='x', y='y', source=tsne_df)
hover = plot_chart.select(dict(type=HoverTool))
hover.tooltips={"word": "@words"}
show(plot_chart)

#Save word embedding model
model_file = 'imdb_word2vec_embedding.txt'
model.wv.save_word2vec_format(filename, binary=False)