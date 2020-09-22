from django.core.management.base import BaseCommand, CommandError
from .job_boards import indeed, monster
from scraper.models import *

class Command(BaseCommand):
   
    def handle(self, *args, **options):
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
            total_jobs = total_jobs + monster_jobs + indeed_jobs 

            
        for job in total_jobs:  
            print(f'Saving job id {job["job_id"]} in database')
            print(f'Title: {job["title"]}')
            print(f'Company: {job["company"]}')
            print(f'Url: {job["href"]}')
            company = Company.objects.get_or_create(name=job["company"])[0]
            job_board = JobBoard.objects.get_or_create(name= job["job_type"])[0]
            try:
                JobsCanada.objects.create(
                    job_id=job["job_id"],
                    title=job["title"],
                    url=job["href"],
                    description=job["description"],
                    location="",
                    company=company,
                    jobBoard= job_board
                )
                print('%s added' % (job["title"],))
            except:
                print("Job already exist!")
            print('\n')
                    