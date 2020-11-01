import pandas as pd
import numpy as np
import pickle 
from nltk.corpus import stopwords
from gensim.models import word2vec
import nltk.data
import re
import logging
import gensim.models.keyedvectors as word2vec
import time
from scipy import spatial
start = time.time()

with open("prep_data_tokens_underscore_1", "rb") as g:
	data_dice = pickle.load(g)

data_must_have = pd.read_csv('mustHaveSkills-2.csv', header = 0, encoding='ISO-8859-1')
del data_must_have['job_brief_id']

data_must_have = data_must_have.drop_duplicates(subset=['keyword_name', 'job_title'], keep='last')
data_must_have = data_must_have[data_must_have["job_title"] != 0]
data_must_have.drop_duplicates(inplace=True)
data_must_have['keyword_name'] = data_must_have['keyword_name'].str.lower()
data_must_have['keyword_name'] = data_must_have['keyword_name'].str.replace(' ' ,'_')
data_must_have['job_title'] = data_must_have['job_title'].str.lower()
gr_df_jobtitle = data_must_have.groupby('job_title')['keyword_name'].apply(list)

must_have_data = []
for vector_list in gr_df_jobtitle:
	xx = list(set(vector_list))
	if xx not in must_have_data:
		must_have_data.append(xx)
print (len(must_have_data))


data_naruki = pd.read_csv('naukri_skill_full', header = 0, encoding='ISO-8859-1')
data_naruki.drop_duplicates(subset=['id', 'skill'], keep='last')
data_naruki['skill'] = data_naruki['skill'].str.lower()
data_naruki['skill'] = data_naruki['skill'].str.replace(' ','_')
data_naruki_final = data_naruki.groupby('id')['skill'].apply(list)


data_train_w2v = data_dice
for must_have in gr_df_jobtitle:
	if len(must_have) > 2:
		if must_have not in data_train_w2v:
			data_train_w2v.append(must_have)

for skills in data_naruki_final:
	if len(skills) > 2 and skills not in data_train_w2v:
		data_train_w2v.append(skills)

print ("Saving...")
with open('./duyet_data_train_w2v', 'wb') as f:
	pickle.dump(data_train_w2v, f)
with open('./duyet_data_train_w2v', 'rb') as f:
	data_train_w2v = pickle.load(f)
print ("Saving Done")
data_train_w2v_for_check = data_train_w2v
data_train_w2v = []

for i in data_train_w2v_for_check:
	vector =[]
	for j in i:
		if isinstance(j, str):
			if 1 == 1:
				vector.append(j)
	if i not in data_train_w2v:
		data_train_w2v.append(vector)
print ("Starting to train Model - ")

import multiprocessing
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)    
print ("Training model...")
model = word2vec.Word2Vec(data_train_w2v, 
		  workers=multiprocessing.cpu_count(),  # Number of threads to run in parallel
		  size=300, 
		  min_count=1, 
		  window=10, 
		  sample = 1e-3,  # Downsample setting for frequent words
		  iter=4,
		  sg =1
	)

model.init_sims(replace=True)

model.wv.save_word2vec_format('duyet_word2vec_skill.bin', binary=True)

def avg_feature_vector(words, model, num_features):
		#function to average all words vectors in a given paragraph
		featureVec = np.zeros((num_features,), dtype="float32")
		nwords = 0

		#list containing names of words in the vocabulary
		index2word_set = set(model.index2word) # this is moved as input param for performance reasons
		for word in words:
			if word in index2word_set:
				nwords = nwords+1
				featureVec = np.add(featureVec, model[word])

		if(nwords>0):
			featureVec = np.divide(featureVec, nwords)
		return featureVec

def compare_two_list_skills(skills_1, skills_2):
	sentence_1_avg_vector = avg_feature_vector(skills_1.split(), model=model, num_features=300)
	sentence_2_avg_vector = avg_feature_vector(skills_2.split(), model=model, num_features=300)
	sen1_sen2_similarity =  1 - spatial.distance.cosine(sentence_1_avg_vector,sentence_2_avg_vector)
	
	
	return sen1_sen2_similarity

print ("Time Elapsed : ",time.time()-start)
print ("Time Elapsed : ",time.time()-start)
print (model.similar_by_word('javascript'))

print (compare_two_list_skills("javascript", "oop"))
print (compare_two_list_skills("javascript", "object_oriented_programming"))







