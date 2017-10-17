from sklearn.datasets import fetch_20newsgroups

import numpy as np 

from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline 

import nltk
from nltk.stem.snowball import SnowballStemmer

# Train data preprocessing

X_train = fetch_20newsgroups(subset = 'train', shuffle = True)

print(X_train.target_names)
print('\n'.join(X_train.data[0].split('\n')[:3]))
print(X_train.target[:3])
#Test data preprocessing
X_test = fetch_20newsgroups(subset = 'test',shuffle = True)

stemmer = SnowballStemmer("english", ignore_stopwords = True)

class StemmedCountVectorizer(CountVectorizer):
	def build_analyzer(self):
		analyzer = super(StemmedCountVectorizer, self).build_analyzer()
		return lambda doc:([stemmer.stem(w) for w in analyzer(doc)])
#it seems that the stemming may lower the accuracy of classification.

stemmed_CountVect = StemmedCountVectorizer(ngram_range=(1,2))
tfidf_tran = TfidfTransformer(use_idf = True)
mnb_clf = MultinomialNB(alpha = 1e-2, fit_prior = False)

text_clf_pipeline = Pipeline([
    ('vect',stemmed_CountVect),
    ('tfidf',tfidf_tran),
    ('mnb',mnb_clf),
    ])
text_clf_pipeline = text_clf_pipeline.fit(X_train.data,X_train.target)
prediction = text_clf_pipeline.predict(X_test.data)
print(np.mean(prediction == X_test.target))
'''
NB_text_clf = Pipeline([('vect',StemmedCountVectorizer(stop_words = 'english')),
						('tfidf', TfidfTransformer()),
						('mnb',MultinomialNB())])

stemmed_parameter = {'vect__ngram_range':[(1,1),(1,2)],
					'tfidf__use_idf':[True,False],
					'mnb__alpha':[1e-2,1e-3],}

model_selection_stemmed = GridSearchCV(NB_text_clf, stemmed_parameter, n_jobs = -1)
model_selection_stemmed = model_selection_stemmed.fit(X_train.data, X_train.target)
print(model_selection_stemmed.best_score_)
print(model_selection_stemmed.best_params_)
'''

