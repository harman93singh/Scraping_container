from decouple import config, Csv
from job_boards import indeed, monster
import pymysql.cursors 

indeed_url = config('INDEED_URL')
total_jobs = []
job_keywords = ['software+developer','software+tester','software+support','software+intern', 'data+engineer','data+scientist','data+analyst','data+entry','data+science']

for keyword in job_keywords:
    print('Getting jobs for ' + keyword)
    indeed_obj = indeed.IndeedJobs('https://ca.indeed.com/jobs?as_and='+ keyword +'&jt=all&l=ontario&fromage=1&limit=50&sort=date&psf=advsrch&from=advancedsearch')
    monster_obj = monster.MonsterJobs('https://www.monster.ca/jobs/search/?q='+ keyword +'&stpage=1&tm=0')
    pageRangeIndeed = indeed_obj.getRange()
    pageRangeMonster = monster_obj.getRange()
    indeed_jobs = indeed_obj.get()
    monster_jobs = monster_obj.get()
    print(f'Saved job listings for ' + keyword + '\n\n')
    total_jobs = total_jobs + indeed_jobs + monster_jobs

for job in total_jobs:
    
    print(f'Title: {job["title"]}')
    print(f'Company: {job["company"]}')
    print(f'Url: {job["href"]}')
    #print(f'Description: {job["description_text"]}')
    print('------------------------------------------------------------------------------')

connection = pymysql.connect(host='sl-us-south-1-portal.42.dblayer.com',
                             database='jobs',
                             user='jobs',
                             password='Stable123',
                             port=23120,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try: 
    cursor = connection.cursor()
    #with connection.cursor() as cursor: 
    for job in total_jobs: 
        #import pdb; pdb.set_trace();
        sql = "INSERT INTO jobscanada(TITLE,COMPANY, COMPANY_URL, DESCRIPTION) VALUES (%s, %s,%s,%s)" 
        cursor.execute(sql,(job['title'], job['company'], job['href'], job['description_text'])) 
        connection.commit() 
finally: 
    connection.close()