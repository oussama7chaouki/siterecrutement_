from rest_framework import serializers
from candidat.models import Experience,Language,Skill,Formation

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = ('user_id', 'experience', 'company', 'startyear', 'endyear')

class FormationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Formation
        fields = ('user_id', 'formation', 'school', 'startyear', 'endyear')

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ('id', 'user_id', 'language')

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ('id', 'user_id', 'skill')

