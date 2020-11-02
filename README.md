# Entity-Extraction-and-Enrichment-from-Job-Ads-and-CV-and-Skill-Matching
1) job_scraper.py - Extract entities from job-ads including company name, job title, location, job description and salary.
2) jobs_extracted.csv - File containing job profiles of 300 companies with above entities extracted out by running job_scraper.py.
3) extract_skills.py - Python file used to extract skills from the job descriptions of the jobs extracted above.
4) skills_extracted.csv - File containing job profiles of 300 companies along with a column of required skills extracted from the job description.
# Files used for skill2vec
1) naukri_skill_full - CSV file containing skills to be used to convert them into vector representation.
2) musthaveskills-2.csv - CSV file containing keywords related to job titles and id.
3) prep_data_tokens_underscore_1 - File used to prepare data and train the model.
4) duyet_data_train_w2v - Trained model saved in a file.
5) duyet_word2vec_skill.bin - Trained model saved in word2vec format.
6) skill2vec.py - Python file used to read related CSV files and train the model.
