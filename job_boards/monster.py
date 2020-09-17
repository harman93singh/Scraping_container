from bs4 import BeautifulSoup
import sys
import math
from job_boards.helpers import HttpHelpers
import re

class MonsterJobs:
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
            count_str = soup.find('h2', class_="figure").get_text()
            max_results = int(count_str.split()[0].replace(',', '').replace('(', ''))
            self.totalJobs = max_results
            max_results = math.ceil(max_results/25)
            self.pageRange = max_results
        except:
            max_results = 0
        return max_results

    def get(self):

        print("Total " + str(self.pageRange)+ " pages to search for " + str(self.totalJobs) +" jobs.")
        monster_jobs = []
        pageRangeCond = (self.pageRange + 1) if (self.pageRange > 10 ) else 11
        for i in range(10, pageRangeCond):
            print('Getting jobs from page ' +  str(i))
            page = self.helpers.download_page(self.url + '&page=' + str(i))

            if page is None:
                sys.exit('indeed, there was an error downloading indeed jobs webpage. cannot continue further, so fix this first')

            monster_jobs = monster_jobs + self.__parse_index(page)

        for job in monster_jobs:
                job_content = self.helpers.download_page(job["href"])
                if job_content is None:
                    continue

                text, des_element = self.__parse_details(job_content)
                job["description_text"] = text
                job["description"] = des_element
        return monster_jobs

    def search_tag(self, tag):
        return tag.has_attr('data-jobid') 

    def __parse_index(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        jobs_container = soup.find(id='ResultsContainer')
        job_items = jobs_container.find_all('section', class_='card-content')
        job_items = [ div for div in job_items if self.search_tag(div)]

        if job_items is None or len(job_items) == 0:
            return []
        
        all_jobs = []

        for job_elem in job_items:
            title_elem = job_elem.find('h2', class_='title')
            company_elem = job_elem.find('div', class_='company')
            url_elem = job_elem.find('a')
            job_id = job_elem.attrs['data-jobid']

            if None in (title_elem, company_elem, url_elem):
                continue

            href = url_elem.get('href')
            if href is None:
                continue

            item = {
                "job_id" : job_id,
                "title" : title_elem.text.strip(),
                "company" : company_elem.text.strip(),
                "href" : href,
                "description" : "",
                "description_text" : ""
            }
            all_jobs.append(item)
        
        return all_jobs
    
    def __parse_details(self, htmlcontent):
        soup = BeautifulSoup(htmlcontent, 'lxml')
        description_element = soup.find('div', class_='job-description')
        try:
            description_text = description_element.text.strip()
            description_text = re.sub("[^a-zA-Z+3]", " ", description_text)
        except:
            description_text = "Sample Text"
        return (description_text, str(description_element))
    