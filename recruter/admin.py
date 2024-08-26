from django.contrib import admin
from .models import Job,Candidature
from shared.models import User
from candidat.models import Skill,Language,Formation,Experience,Information

# Register your models here.
admin.site.register(User)
admin.site.register(Candidature)
admin.site.register(Job)
admin.site.register(Skill)
admin.site.register(Language)
admin.site.register(Formation)
admin.site.register(Experience)
admin.site.register(Information)

