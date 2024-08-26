from django.db import models
from recruter.models import Job

from shared.models import User

# to_add


class Report(models.Model):
    report_id = models.AutoField(primary_key=True)
    candidat = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job,  on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
