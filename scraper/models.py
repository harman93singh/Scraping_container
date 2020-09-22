from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.TextField(max_length=1000)
    url = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class JobBoard(models.Model):
    name = models.TextField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class JobsCanada(models.Model):
    job_id = models.CharField(max_length=254, unique=True)
    title = models.TextField(max_length=1000)
    url = models.TextField(max_length=5000)
    description = models.TextField(max_length=12000)
    location = models.TextField(max_length=1000)
    company= models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company')
    jobBoard= models.ForeignKey(JobBoard, on_delete=models.CASCADE, related_name='jobboard')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title