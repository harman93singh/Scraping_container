from job_boards import indeed, monster
import pymysql.cursors 

total_jobs = []
job_keywords = ['software+developer','software+tester','software+support','software+intern', 'data+engineer','data+scientist','data+analyst','data+entry','data+science']

for keyword in job_keywords:
    indeed_obj = indeed.IndeedJobs('https://ca.indeed.com/jobs?as_and='+ keyword +'&jt=all&l=ontario&fromage=1&limit=50&sort=date&psf=advsrch&from=advancedsearch')
    monster_obj = monster.MonsterJobs('https://www.monster.ca/jobs/search/?q='+ keyword +'&stpage=1&tm=0')
    pageRangeIndeed = indeed_obj.getRange()
    pageRangeMonster = monster_obj.getRange()
    print('\nGetting jobs for ' + keyword.replace('+', " ") +' from indeed.ca')
    indeed_jobs = indeed_obj.get()
    print('Getting jobs for ' + keyword.replace('+', " ") +' from monster.ca')
    monster_jobs = monster_obj.get()
    print(f'Saved job listings for ' + keyword.replace('+', " "))
    total_jobs = total_jobs + indeed_jobs + monster_jobs

connection = pymysql.connect(host='sl-us-south-1-portal.42.dblayer.com',
                             database='jobs',
                             user='jobs',
                             password='Stable123',
                             port=23120,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
try: 
    cursor = connection.cursor()
    for job in total_jobs: 
        try:
            print(f'Saving job id {job["job_id"]} in database')
            print(f'Title: {job["title"]}')
            print(f'Company: {job["company"]}')
            print(f'Url: {job["href"]}')
            print('\n')
            sql = "INSERT INTO jobscanada(JOB_ID, TITLE, COMPANY, COMPANY_URL, DESCRIPTION) VALUES (%s, %s, %s,%s,%s)" 
            cursor.execute(sql,(job['job_id'], job['title'], job['company'], job['href'], job['description_text'])) 
            connection.commit()
        except:
            pass
finally: 
    connection.close()