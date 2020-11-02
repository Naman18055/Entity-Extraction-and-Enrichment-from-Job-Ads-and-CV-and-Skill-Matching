import numpy as np
import gensim.models.keyedvectors as word2vec
from scipy import spatial

def avg_feature_vector(words, model, num_features):
		featureVec = np.zeros((num_features,), dtype="float32")
		nwords = 0
		index2word_set = set(model.index2word) # this is moved as input param for performance reasons
		for word in words:
			if word in index2word_set:
				nwords = nwords+1
				featureVec = np.add(featureVec, model[word])
		if(nwords>0):
			featureVec = np.divide(featureVec, nwords)
		return featureVec

def sum_feature_vector(words, model, num_features):
		featureVec = np.zeros((num_features,), dtype="float32")
		nwords = 0
		index2word_set = set(model.index2word) # this is moved as input param for performance reasons
		for word in words:
			if word in index2word_set:
				nwords = nwords+1
				featureVec = np.add(featureVec, model[word])
		return featureVec
	
def compare_two_list_skills(skills_1, skills_2):
	sentence_1_avg_vector = avg_feature_vector(skills_1.split(), model=model, num_features=300)
	sentence_2_avg_vector = avg_feature_vector(skills_2.split(), model=model, num_features=300)
	sen1_sen2_similarity =  1 - spatial.distance.cosine(sentence_1_avg_vector,sentence_2_avg_vector)
	return sen1_sen2_similarity

def compare_two_list_skills_sum(skills_1, skills_2):
	sentence_1_avg_vector = sum_feature_vector(skills_1.split(), model=model, num_features=300)
	sentence_2_avg_vector = sum_feature_vector(skills_2.split(), model=model, num_features=300)
	sen1_sen2_similarity =  1 - spatial.distance.cosine(sentence_1_avg_vector,sentence_2_avg_vector)
	return sen1_sen2_similarity

model = word2vec.KeyedVectors.load_word2vec_format('duyet_word2vec_skill.bin', binary=True)
print (compare_two_list_skills("java", "c++"))
print (model.similar_by_word("java"))
