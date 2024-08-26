from rest_framework.decorators import api_view
from rest_framework.response import Response
from recruter.models import Job,Candidature
from .serializers import JobSerializer,JobSerializers
from recruter.api import serializers
from rest_framework import status
from django.http import JsonResponse
from candidat.models import Skill,Language,Formation,Experience,Profile
from .serializers import SkillSerializer, LanguageSerializer, FormationSerializer, ExperienceSerializer, InformationSerializer
from shared.models import User

@api_view(['GET'])
def getJobs(request):
    room = Job.objects.all()
    serializer = JobSerializer(room, many=True)
    return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def getJob(request, pk):
    room = Job.objects.get(id_job=pk)
    if request.method == 'GET':
        serializer = JobSerializer(room, many=False)
        data = {
            'data': serializer.data,
            'status':status.HTTP_200_OK
        }
        return Response(data)
    elif request.method == 'PUT':
        serializer = JobSerializers(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":status.HTTP_201_CREATED})
        return Response({"error":serializer.errors, "status":status.HTTP_400_BAD_REQUEST})

    elif request.method == 'DELETE':
        room.delete()
        return Response({"status":status.HTTP_204_NO_CONTENT})

@api_view(['POST'])
def sendJob(request):
        serializer = JobSerializers(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response({"status":status.HTTP_201_CREATED})
        return Response({"error":serializer.errors, "status":status.HTTP_400_BAD_REQUEST})

@api_view(['POST'])
def accept_candidature(request):
    if request.method == 'POST':
        id_candidature = request.POST.get('id_candidature')

        try:
            candidature = Candidature.objects.get(id_candidature=id_candidature)
            candidat_id = candidature.candidat
            
            candidature.status = 'Accepted'
            candidature.save()

            res = {
                'status': 200,
                'message': 'Candidate accepted successfully'
            }
            return JsonResponse(res)
        except Candidature.DoesNotExist:
            res = {
                'status': 500,
                'message': 'Candidature does not exist'
            }
            return JsonResponse(res)
        except Exception as e:
            res = {
                'status': 500,
                'message': str(e)
            }
            return JsonResponse(res)
    else:
        res = {
            'status': 500,
            'message': 'Invalid request method'
        }
        return JsonResponse(res)

@api_view(['POST'])
def reject_candidature(request):
    if request.method == 'POST':
        id_candidature = request.POST.get('id_candidature')

        try:
            candidature = Candidature.objects.get(id_candidature=id_candidature)
            candidature.status = 'Rejected'
            candidature.save()


            res = {
                'status': 200,
                'message': 'Candidate rejected successfully'
            }
            return JsonResponse(res)
        except Candidature.DoesNotExist:
            res = {
                'status': 500,
                'message': 'Candidature does not exist'
            }
            return JsonResponse(res)
        except Exception as e:
            res = {
                'status': 500,
                'message': str(e)
            }
            return JsonResponse(res)
    else:
        res = {
            'status': 500,
            'message': 'Invalid request method'
        }
        return JsonResponse(res)
    
def fetch_user(request):
    if request.method == 'POST':
        user_id= request.POST.get('user_id')
        user_skills = Skill.objects.filter(user_id=user_id)
        user_languages = Language.objects.filter(user_id=user_id)
        user_formations = Formation.objects.filter(user_id=user_id)
        user_experiences = Experience.objects.filter(user_id=user_id)
        user_information = Profile.objects.filter(candidat_id_id=user_id)

        skill_serializer = SkillSerializer(user_skills, many=True)
        language_serializer = LanguageSerializer(user_languages, many=True)
        formation_serializer = FormationSerializer(user_formations, many=True)
        experience_serializer = ExperienceSerializer(user_experiences, many=True)
        information_serializer = InformationSerializer(user_information, many=True)

        response = {
            'array0': information_serializer.data,
            'array1': formation_serializer.data,
            'array2': experience_serializer.data,
            'array3': skill_serializer.data,
            'array4': language_serializer.data,
        }

        return JsonResponse(response)
