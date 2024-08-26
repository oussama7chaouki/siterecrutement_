from django.shortcuts import render, redirect
from shared.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from .models import Skill,Language,Formation,Experience,Information,Profile
from recruter.models import Candidature,Job
from appadmin.models import Report
from django.http import JsonResponse
# Import Pagination Stuff
from django.core.paginator import Paginator
from django.db.models import Subquery, OuterRef,Exists
from .cvparser.cvparser import cvparser


def user_role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                if request.user.role == 2:
                    return redirect('/admin/')
                
                else:
                    return redirect('/recruter/')
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

# Import Pagination Stuff
from django.core.paginator import Paginator
def loginPage(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'candidat/login.html', context)

                 # Check if the user's role is not equal to 1
        if user.role != 0:
            messages.error(request, 'You do not have permission to login')
            return render(request, 'candidat/login.html', context)
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'candidat/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginc')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.role=0
            user.save()
            login(request, user)
            return redirect('home')
        else:
            # Accessing errors for all fields in the form
            for field in form.fields.keys():
                field_error = form.errors.get(field)
                if field_error:
                    # Return a specific error message for the field
                    messages.error(request, f"Error in {field} field: {field_error}")

    return render(request, 'candidat/login.html', {'form': form})

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def home(request):
    jobs_not_applied = Job.objects.exclude(
        id_job__in=Candidature.objects.filter(candidat=request.user).values('job_id')
    ).order_by('date')

    context = {"jobs": jobs_not_applied}
    return render(request, 'candidat/home.html', context)

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def apply(request,pk):
    jobapp = Job.objects.get(id_job=pk)
    candidature = Candidature(candidat = request.user ,job = jobapp, reqexp = jobapp.expreq, reqfor = jobapp.formationreq,reqskill = jobapp.skillreq)
    candidature.save()
    return redirect('home')

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def report(request,pk):
    jobapp = Job.objects.get(id_job=pk)
    report = Report(candidat = request.user ,job = jobapp)
    report.save()
    return redirect('candidature')

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def report1(request,pk):
    jobapp = Job.objects.get(id_job=pk)
    report = Report(candidat = request.user ,job = jobapp)
    report.save()
    return redirect('home')

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def compte(request):
    user_id = request.user
    experience=Experience.objects.filter(user_id=user_id)
    formation=Formation.objects.filter(user_id=user_id)
    #  print(formation)
    print(experience)
    skill=Skill.objects.filter(user_id=user_id)
    language=Language.objects.filter(user_id=user_id)
    context = {
            'experience': experience,
            'formation':formation,
            'skill':skill,
            'language':language,
        }
    return render(request, 'candidat/compte.html',context)

@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def candidature(request):
    
    candidatures_non_signalees = Candidature.objects.filter(
        candidat=request.user
    ).exclude(
        Exists(Report.objects.filter(job_id=OuterRef('job_id'), candidat=request.user))
    ).values(
        'id_candidature', 'job_id', 'date', 'job__job_title', 'job__recruter__name', 'status'
    )

    context = {
        'candidatures': candidatures_non_signalees,
    }  
    return render(request, 'candidat/candidature.html', context)
from django.http import JsonResponse
@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def delete_candidature(request):
    if request.method == 'POST':
        candidature_id = request.POST.get('id_candidature')
        try:
            candidature = Candidature.objects.get(id_candidature=candidature_id)
            candidature.delete()
            return JsonResponse({'status': 'success'})
        except Candidature.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Candidature not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def view_score(request, candidature_id):
    candidature = Candidature.objects.filter(id_candidature=candidature_id).first()
    
    if candidature is not None:
        # Extract relevant data from the candidature
        score_data = {
            'score': candidature.score,
            'reqfor': candidature.reqfor,
            'reqexp': candidature.reqexp,
            'reqskill': candidature.reqskill,
        }

        return JsonResponse(score_data)
    else:
        return JsonResponse({'error': 'Candidature not found'}, status=404)

       
@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def profile_details(request):
    user_id = request.user # Assuming you have the user ID in the session

    try:
        profile = Profile.objects.get(candidat_id=user_id)
    except Profile.DoesNotExist:
        return redirect('profile_form')
    
    context = {
        'profile': profile,
        'email': request.user.email

    }

    return render(request, 'candidat/settings.html', context)
@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def profile_form(request):
    user_id = request.user
    username=request.user.username


    if request.method == 'POST':
        # Récupérez les données du formulaire
        last_name = request.POST.get('nom')
        name = request.POST.get('prenom')
        email=request.POST.get('email')
        date_naissance = request.POST.get('date')
        genre = request.POST.get('genre')
        ville = request.POST.get('ville')
        pays=request.POST.get('pays')
        tel = request.POST.get('tel')
        domaine = request.POST.get('select')
        avatar= request.FILES['avatar']
 # Extract file extension (e.g., jpg, png)
        file_extension = avatar.name.split('.')[-1]
        new_filename = f"{username}_avatar.{file_extension}"
        # Récupérez l'utilisateur actuel
        # Ajout de '.id' pour obtenir l'ID de l'utilisateur

        try:
            profile = Profile.objects.get(candidat_id=user_id)
            user = User.objects.get(id=user_id.id)
            # Modifier le profil existant
            profile.last_name = last_name
            profile.name = name
            user.email=email
            profile.date_naissance = date_naissance
            profile.genre = genre
            profile.ville = ville
            profile.pays=pays
            profile.tel = tel
            profile.domaine = domaine
            user.avatar=avatar
            user.avatar.save(new_filename, avatar)
            profile.save()
        except Profile.DoesNotExist:
            # Créer un nouveau profil
            profile = Profile.objects.create(
                last_name=last_name,
                name=name,
                email=email,
                date_naissance=date_naissance,
                genre=genre,
                ville=ville,
                pays=pays,
                tel=tel,
                domaine=domaine,
                candidat_id=user_id
            )

            
            
        return JsonResponse({'status': 'success'})

    else:
        # Si la méthode n'est pas POST, récupérez le profil existant ou créez un nouveau
        try:
            profile = Profile.objects.get(candidat_id=user_id)
            user = User.objects.get(id=user_id.id)

        except Profile.DoesNotExist:
            profile = {
                "last_name": " ",
                "name": " ",
                "email":" ",
                "date_naissance": " ",
                "genre": " ",
                "ville": " ",
                "pays":"pays",
                "tel": " ",
                "domaine": " ",
            }

    context = {
        'profile': profile,
         'email': user_id.email
    }

   
        # If it's a regular form submission, render the HTML template
    return render(request, 'candidat/profilcandidat.html', context)
@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def listReport(request):
    reports = Report.objects.all().order_by('date')
    context = {"reports":reports}
    return render(request,'candidat/report.html',context)


@login_required(login_url='/candidat/login')
@user_role_required(role=0)
def cvupload(request):
    user_id = request.user
    username=user_id.username
    if request.method == 'POST':
        uploaded_file = request.FILES['cv_file']
        profile = Profile.objects.get(candidat_id=user_id)
        if uploaded_file:
            file_extension = uploaded_file.name.split('.')[-1]
            new_filename = f"{username}_cv.{file_extension}"
            if(profile.cv):
                profile.cv.delete()
            profile.cv.save(new_filename, uploaded_file)
            profile.save()
            # Pass the uploaded file to the CV parsing function
            parsed_data = cvparser("static/img/profiles/cv/"+new_filename)
            formations_data, experiences_data, skill_data, language_data=parsed_data
            insert_user_data(user_id, formations_data, experiences_data, skill_data, language_data)
            # For demonstration purposes, print parsed data in console
            return JsonResponse({'status': 'success'})  # You can customize the response
    return render(request, 'candidat/cvupload.html')

def insert_user_data(user, formations_data, experiences_data, skill_data, language_data):

    # Delete existing formations, experiences, skills, and languages for this user
    Formation.objects.filter(user_id=user).delete()
    Experience.objects.filter(user_id=user).delete()
    Skill.objects.filter(user_id=user).delete()
    Language.objects.filter(user_id=user).delete()

    # Insert formations
    for formation_data in formations_data:
        formation_data['user_id'] = user
        Formation.objects.create(**formation_data)

    # Insert experiences
    for experience_data in experiences_data:
        experience_data['user_id'] = user
        Experience.objects.create(**experience_data)

    # Insert skills
    skill_data['user_id'] = user
    Skill.objects.create(**skill_data)

    # Insert languages
    language_data['user_id'] = user
    Language.objects.create(**language_data)