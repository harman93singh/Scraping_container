from decouple import config, Csv
from job_boards import indeed

indeed_url = 'https://ca.indeed.com/jobs?as_and=software&jt=all&l=ontario&fromage=1&limit=50&sort=date&psf=advsrch&from=advancedsearch'

print('Getting jobs from indeed.com')
indeed = indeed.IndeedJobs(indeed_url)
pageRange = indeed.getRange()
indeed_jobs = indeed.get()
print(f'Found {len(indeed_jobs)} job listings within the specified criteria')

for job in indeed_jobs:
    
    print(f'Title: {job["title"]}')
    print(f'Company: {job["company"]}')
    print(f'Url: {job["href"]}')
    print(f'Description: {job["description_text"]}')
    print('------------------------------------------------------------------------------')