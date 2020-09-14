from decouple import config, Csv
from job_boards import indeed

indeed_url = config('INDEED_URL')
total_jobs = []
job_keywords = ['software+developer', 'software+engineer','software+tester','software+support','software+intern',
'data+engineer','data+scientist','data+analyst','data+entry','data+science']

for keyword in job_keywords:
    print('Getting jobs for ' + keyword)
    indeed_obj = indeed.IndeedJobs('https://ca.indeed.com/jobs?as_and='+ keyword +'&jt=all&l=ontario&fromage=1&limit=50&sort=date&psf=advsrch&from=advancedsearch')
    pageRange = indeed_obj.getRange()
    indeed_jobs = indeed_obj.get()
    print(f'Saved job listings for ' + keyword + '\n\n')
    total_jobs = total_jobs + indeed_jobs

for job in total_jobs:
    
    print(f'Title: {job["title"]}')
    print(f'Company: {job["company"]}')
    print(f'Url: {job["href"]}')
    print(f'Description: {job["description_text"]}')
    print('------------------------------------------------------------------------------')