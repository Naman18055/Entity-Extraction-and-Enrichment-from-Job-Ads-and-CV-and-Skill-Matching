import pandas as pd
import spacy
import time
import csv
import pickle
from spacy.matcher import PhraseMatcher

# LOADING SKILLS IN MATCHER
start = time.time()
skills = pd.read_csv('skills', sep='\n', header=None)

nlp = spacy.load("en_core_web_sm")
print("Making skill words")
skill_words = [nlp(text) for text in skills[0].dropna(axis=0)]
print("Done")

matcher = PhraseMatcher(nlp.vocab)
matcher.add('Skills', None, *skill_words)
print("Skills loaded in matcher")
print ("Total time taken to load skills : ",time.time()-start)

# EXTRACT SKILLS FROM THE JOB DESCRIPTION
def get_skills(t2):
	doc = nlp(t2)
	matches = matcher(doc)
	done = set()
	for match_id, start, end in matches:
		rule_id = nlp.vocab.strings[match_id]  # get the unicode ID, i.e. 'COLOR'
		span = doc[start: end]  # get the matched slice of the doc
		if span.text not in done:
			done.add(span.text)
	return ",".join(map(str,list(done)))

# ADDING A COLUMN OF SKILLS REQUIRED TO THE CSV FILE
df = pd.read_csv("test.csv")
print (len(df["Location"]))
with open("test.csv","r") as inp:
	with open("job.csv","w") as out:
		writer = csv.writer(out)
		reader = csv.reader(inp)
		fin = []
		row = next(reader)
		row.append("Required Skills")
		fin.append(row)
		count = 0 
		for row in reader:
			text = row[2]
			skills = get_skills(text)
			row.append(skills)
			fin.append(row)
			count += 1
			print (count)			

		writer.writerows(fin)