from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from candidat.models import Formation,Experience,Language,Skill
from .serializers import FormationSerializer,ExperienceSerializer,LanguageSerializer,SkillSerializer
@api_view(['POST'])
def create_formation(request):
    serializer = FormationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 200, 'message': 'Formation Created Successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_formation(request, formation_id):
    try:
        formation = Formation.objects.get(id=formation_id)
    except Formation.DoesNotExist:
        return Response({'status': 404, 'message': 'Formation ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = FormationSerializer(data=request.data)
    if serializer.is_valid():
        formation.formation = serializer.validated_data.get('formation', formation.formation)
        formation.school = serializer.validated_data.get('school', formation.school)
        formation.startyear = serializer.validated_data.get('startyear', formation.startyear)
        formation.endyear = serializer.validated_data.get('endyear', formation.endyear)
        formation.save()
        return Response({'status': 200, 'message': 'Formation Updated Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_formation(request, formation_id):
    try:
        formation = Formation.objects.get(id=formation_id)
        serializer = FormationSerializer(formation)
        return Response({'status': 200, 'message': 'Formation Fetched Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Formation.DoesNotExist:
        return Response({'status': 404, 'message': 'Formation ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_formation(request, formation_id):
    try:
        formation = Formation.objects.get(id=formation_id)
        formation.delete()
        return Response({'status': 200, 'message': 'Formation Deleted Successfully'}, status=status.HTTP_200_OK)
    except Formation.DoesNotExist:
        return Response({'status': 404, 'message': 'Formation ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def create_experience(request):
    serializer = ExperienceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # Assuming user_id is available in the request
        return Response({'status': 200, 'message': 'Experience Created Successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
def update_experience(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
    except Experience.DoesNotExist:
        return Response({'status': 404, 'message': 'Experience ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = ExperienceSerializer(experience, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status': 200, 'message': 'Experience Updated Successfully'}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_experience(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
        serializer = ExperienceSerializer(experience)
        return Response({'status': 200, 'message': 'Experience Fetched Successfully', 'data': serializer.data}, status=status.HTTP_200_OK)
    except Experience.DoesNotExist:
        return Response({'status': 404, 'message': 'Experience ID Not Found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_experience(request, experience_id):
    try:
        experience = Experience.objects.get(id=experience_id)
        experience.delete()
        return Response({'status': 200, 'message': 'Experience Deleted Successfully'}, status=status.HTTP_200_OK)
    except Experience.DoesNotExist:
        return Response({'status': 404, 'message': 'Experience ID Not Found'}, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST'])
def save_language(request):
    user_id = request.user  # Assuming user_id is available in the request
    language = request.data.get('language')

    existing_language = Language.objects.filter(user_id=user_id).first()
    if existing_language:
        existing_language.language = language
        existing_language.save()
    else:
        Language.objects.create(user_id=user_id, language=language)

    return Response({'message': 'Your data has been successfully saved into System'}, status=status.HTTP_200_OK)

@api_view(['POST'])
def save_skill(request):
    user_id = request.user  # Assuming user_id is available in the request
    skill = request.data.get('skill')

    existing_skill = Skill.objects.filter(user_id=user_id).first()
    if existing_skill:
        existing_skill.skill = skill
        existing_skill.save()
    else:
        Skill.objects.create(user_id=user_id, skill=skill)

    return Response({'message': 'Your data has been successfully saved into System'}, status=status.HTTP_200_OK)