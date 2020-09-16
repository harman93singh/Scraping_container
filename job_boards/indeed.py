from bs4 import BeautifulSoup
import sys
import math
import re

from job_boards.helpers import HttpHelpers

class IndeedJobs:
    def __init__(self, url):
        self.url = url
        self.helpers = HttpHelpers()
        self.pageRange = 0
        self.totalJobs = 0

    def getRange(self):
        page = self.helpers.download_page(self.url)
        if page is None:
            sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')
        soup = BeautifulSoup(page, 'lxml')
        try:
            count_str = soup.find('div', id="searchCountPages").get_text()
            max_results = int(count_str.split()[3].replace(',', ''))
            self.totalJobs = max_results
            max_results = math.ceil(max_results/50)
            self.pageRange = max_results
        except:
            max_results = 0
        return max_results

    def get(self):
        print("Total " + str(self.pageRange)+ " pages to search for " + str(self.totalJobs) +" jobs.")
        indeed_jobs = []
        for i in range(0,self.pageRange * 50,50):
            print('Getting jobs from page ' +  str(int(i/50) + 1))
            page = self.helpers.download_page(self.url + "&start="+ str(i))

            if page is None:
                sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')

            indeed_jobs = indeed_jobs + self.__parse_index(page)

        for job in indeed_jobs:
                job_content = self.helpers.download_page(job["href"])
                if job_content is None:
                    continue

                text, des_element = self.__parse_details(job_content)
                job["description_text"] = text
                job["description"] = des_element
        return indeed_jobs

    def __parse_index(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        jobs_container = soup.find(id='resultsCol')
        job_items = jobs_container.find_all('div', class_='jobsearch-SerpJobCard')

        if job_items is None or len(job_items) == 0:
            return []
        
        all_jobs = []

        for job_elem in job_items:
            url_elem = job_elem.find('a', class_='jobtitle')
            title_elem = job_elem.find('a', class_='jobtitle')
            company_elem = job_elem.find('span', class_='company')

            if None in (title_elem, company_elem, url_elem):
                continue

            href = url_elem.get('href')
            if href is None:
                continue

            item = {
                "title" : title_elem.text.strip(),
                "company" : company_elem.text.strip(),
                "href" : f'https://www.indeed.com{href}',
                "description" : "",
                "description_text" : ""
            }
            all_jobs.append(item)
        
        return all_jobs

    def __parse_details(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        description_element = soup.find(id='jobDescriptionText')
        try:
            description_text = description_element.text.strip()
            description_text = re.sub("[^a-zA-Z+3]", " ", description_text)
        except:
            description_text = "Could not find any description"

        return (description_text, str(description_element))