from rest_framework.serializers import ModelSerializer
from recruter.models import Job
from candidat.models import Skill,Language,Formation,Experience,Information,Profile




class JobSerializer(ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'

class JobSerializers(ModelSerializer):
    class Meta:
        model = Job
        fields = (
            'job_title',
            'job_salaire',
            'domain',
            'formationreq',
            'expreq',
            'skillreq',
            'job_description',
            'recruter'
        )
class SkillSerializer(ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

class LanguageSerializer(ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'

class FormationSerializer(ModelSerializer):
    class Meta:
        model = Formation
        fields = '__all__'

class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'

class InformationSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

