from django.forms import JSONField
from django.shortcuts import render, redirect
from shared.models import User
from .models import Job,Candidature,Company
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q,Count,Subquery, OuterRef
from django.contrib.auth import authenticate, login, logout
from .forms import MyUserCreationForm
from django.db import transaction

# Import Pagination Stuff
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse

# Define the custom decorator
def user_role_required(role):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.role != role:
                if request.user.role == 2:
                    return redirect('/admin/')
                else:
                    return redirect('/candidat/')
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator

@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def offer(request):
 user = request.user  # Get the logged-in user
 job_list = Job.objects.filter(recruter=user).order_by('-id_job')
 p = Paginator(Job.objects.filter(recruter=user).order_by('-id_job'), 5)
 page = request.GET.get('page')
 jobs = p.get_page(page)
 nums = "a" * jobs.paginator.num_pages
 user_id = request.user.id
 return render(request, 'recruter/jobs.html', 
		{'job_list': job_list,
		'offers': jobs,
		'nums':nums
        ,'recruter': user_id}
		)
#  offers = [
#     {"id": 1, "title": "Software Engineer", "domain": "Information Technology", "date": "2023-11-28"},
#     {"id": 2, "title": "Financial Analyst", "domain": "Finance", "date": "2023-11-25"},
#     {"id": 3, "title": "Marketing Manscorer", "domain": "Marketing", "date": "2023-11-20"},
#     ]
 
@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def jobcans(request):
 user = request.user  # Get the logged-in user
 job_list = Job.objects.filter(recruter=user).order_by('-id_job')
 p = Paginator(Job.objects.filter(recruter=user).order_by('-id_job'), 4)
 page = request.GET.get('page')
 jobs = p.get_page(page)
 nums = "a" * jobs.paginator.num_pages
 count_total = {}
 for job in job_list:
    count_total[job.id_job] = Candidature.objects.filter(job=job).count()

 return render(request, 'recruter/jobcans.html', 
		{'job_list': job_list,
		'jobcans': jobs,
		'nums':nums,
        'counts': count_total
        }
		)
@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def jobcan(request,pk):
    job=Job.objects.get(id_job=pk)
    candidatures = Candidature.objects.filter(job=job)
    print(candidatures)
    context = {'datas': candidatures}
    return render(request, 'recruter/jobcan.html',context)

def loginPage(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('offer')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'recruter/login.html', context)

                 # Check if the user's role is not equal to 1
        if user.role != 1:
            messages.error(request, 'You do not have permission to login')
            return render(request, 'recruter/login.html', context)
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('offer')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'recruter/login.html', context)

@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def logoutUser(request):
    logout(request)
    return redirect('login')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('offer')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'recruter/login.html', {'form': form})
@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def company_details(request):
    user_id = request.user  # Assuming you have the rec_id in the session

    try:
        company = Company.objects.get(rec_id=user_id)
    except Company.DoesNotExist:
        return redirect('updatecom')

    context = {
        'company': company,
    }

    return render(request, 'recruter/settings.html', context)
@login_required(login_url='/recruter/login')
@user_role_required(role=1)
def update_details(request):
    user_id = request.user
    username = request.user.username

    if request.method == 'POST':
        name = request.POST.get('name')
        person_name = request.POST.get('Contact_Person_name')
        person_email = request.POST.get('Contact_Person_email')
        phone_number = request.POST.get('tel')
        address = request.POST.get('address')
        pays = request.POST.get('pays')
        avatar = request.FILES['avatar1']
  # Extract file extension (e.g., jpg, png)
        file_extension = avatar.name.split('.')[-1]
        new_filename = f"{username}_avatar.{file_extension}"

        # Check if the company exists
        try:
            company = Company.objects.get(rec_id=user_id)
            user = User.objects.get(id=user_id.id)
            # Modify existing company
            company.name=name
            company.person_name = person_name
            company.person_email = person_email
            company.tel = phone_number
            company.address = address
            company.pays=pays
            company.save()
            user.avatar.save(new_filename, avatar)
            user.save()

        except Company.DoesNotExist:
            # Create a new company
            company = Company.objects.create(
                name=name,
                person_name=person_name,
                person_email=person_email,
                tel=phone_number,
                address=address,
                rec_id=user_id,
                pays=pays

            )
        
        # Redirect or render a success page
        return JsonResponse({'status': 'success'})

    try:
        company = Company.objects.get(rec_id=user_id)
    except Company.DoesNotExist:
        company={
  "name": "",
  "Contact_Person_name": "",
  "Contact_Person_email": "",
  "tel": "",
  "address": "",
  "pays":""}

    context = {
        'company': company,
    }

    return render(request, 'recruter/modify.html', context)        
@transaction.atomic
def create_thread(request):
    if request.method == 'POST':
        candidat_id = request.POST.get('id_candidat')
        try:
            # Retrieve the User instance based on candidat_id
            candidat_user = User.objects.get(pk=candidat_id)
            
            # Assuming Thread model has 'first_person' and 'second_person' fields
            thread_exists = Thread.objects.filter(first_person=request.user, second_person=candidat_user).exists()
            print(candidat_id, thread_exists)
            if not thread_exists:
                 # Create a new thread
                thread = Thread.objects.create(first_person=request.user, second_person=candidat_user)
            # # Create a chat message
            else:
               thread=Thread.objects.get(first_person=request.user, second_person=candidat_user)
            if thread: 
             return JsonResponse({'status': 'success'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid candidat ID'})
        except Exception as e:
            # Log the exception for debugging purposes
            print(f"Error creating thread: {e}")
            return JsonResponse({'status': 'error', 'message': 'Thread not created'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})