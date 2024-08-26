from django.db import models
from shared.models import User
# Create your models here.
class Job(models.Model):
    id_job = models.AutoField(primary_key=True)
    recruter = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=55)
    company = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255)
    job_description = models.TextField()
    job_salaire = models.IntegerField()
    date = models.DateField(auto_now_add=True)
    formationreq = models.CharField(max_length=100)
    expreq = models.IntegerField()
    skillreq = models.CharField(max_length=255)
    reportnum  = models.IntegerField(null=True,blank=True)
class Candidature(models.Model):
    id_candidature = models.AutoField(primary_key=True)
    candidat = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    score = models.IntegerField(default=0)
    reqexp = models.CharField(max_length=50)
    reqfor = models.CharField(max_length=50)
    reqskill = models.CharField(max_length=100)
    status = models.CharField(max_length=100, default='Waiting')
class Company(models.Model):
    name = models.CharField(max_length=255)
    person_name = models.CharField(max_length=255)
    pays = models.CharField(max_length=255,null=True)

    person_email = models.EmailField(max_length=255)
    tel = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    rec_id = models.ForeignKey(User, on_delete=models.CASCADE)