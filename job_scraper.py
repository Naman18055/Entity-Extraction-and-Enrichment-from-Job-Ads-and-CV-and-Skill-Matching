from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import pandas as pd
from bs4 import BeautifulSoup
import time

Required_Jobs=300

used_jobs = set()

driver = webdriver.Chrome("./chromedriver")

dataframe = pd.DataFrame(columns =["Company Name","Job Title","Description","Location","Salary"])
driver.get("https://www.glassdoor.co.in/Job/software-developer-jobs-SRCH_KO0,18.htm?jobType=fulltime&employerSizes=5")
total_jobs_searched = 0
while(len(dataframe)<Required_Jobs):
	company_name=""
	job_title=""
	job_desc=""
	time.sleep(4)

	try:
		driver.find_element_by_xpath('//*[@id="MainCol"]/div[1]/ul/li[1]').click()
	except ElementClickInterceptedException:
		print("Unable to find selected")
		pass

	time.sleep(2)

	try:
		driver.find_element_by_class_name("modal_closeIcon").click()
	except NoSuchElementException:
		pass

	all_jobs = driver.find_elements_by_class_name("react-job-listing")
	for job in all_jobs:
		try:
			job.click()
			time.sleep(1)
			collected_successfully = False
		except Exception as e:
			print(e)

		while not collected_successfully:

			try:
				company = driver.find_elements_by_class_name("empInfo")[0]
				soup = BeautifulSoup(company.get_attribute('innerHTML'),'html.parser')
				company_name = soup.find("div",class_="employerName").text[:-3]
				job_location = soup.find("div",class_="location").text
				job_title = soup.find("div",class_="title").text
				desc = driver.find_element_by_class_name("jobDescriptionContent")
				soup = BeautifulSoup(desc.get_attribute('outerHTML'),'html.parser')
				job_desc = soup.find("div",class_="jobDescriptionContent").text
				collected_successfully=True
			except :
				time.sleep(3)

		# try:
		job_salary = None
		driver.find_element_by_xpath('//*[@Data-tab-type="salary"]').click()
		time.sleep(0.5)
		salary_job_title = driver.find_elements_by_class_name("expandHH")
		for salary in salary_job_title:
			soup = BeautifulSoup(salary.get_attribute('innerHTML'),'html.parser')
			title_name = soup.find("div",class_="jobTitle strong").text
			# print (title_name,job_title)
			if (title_name in job_title):
				job_salary = soup.find("div",class_="strong margVertXs").text
				break

		total_jobs_searched += 1
		if not job_salary or "₹ 0" in job_salary:
			continue
		
		if (company_name,job_title,job_desc,job_location,job_salary) not in used_jobs:
			dataframe = dataframe.append({
				"Company Name":company_name,
				"Job Title":job_title,
				"Description":job_desc,
				"Location":job_location,
				"Salary":job_salary
			},ignore_index=True)
			used_jobs.add((company_name,job_title,job_desc,job_location))
			print (company_name,job_title,job_location,job_salary)
			print(len(dataframe),total_jobs_searched)
		if len(dataframe)>=Required_Jobs:
			break
	
	try:
		driver.find_element_by_xpath('//*[@id="FooterPageNav"]/div/ul/li[7]/a').click()
	except NoSuchElementException:
		print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
		break

print ("Total Jobs Searched : ",total_jobs_searched)
dataframe.to_csv("test.csv",index=False)
print(dataframe)