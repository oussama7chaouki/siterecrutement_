from django.shortcuts import get_object_or_404, render
# Create your views here.
from django.shortcuts import render, redirect
from appadmin.models import Report
from shared.models import User
from django.shortcuts import render, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from recruter.models import Candidature
from django.http import JsonResponse
from .forms import MyUserCreationForm
from django.http import HttpResponseRedirect

# Import Pagination Stuff
from django.core.paginator import Paginator


def loginPage(request):
    page = 'login'
    context = {'page': page}

    if request.user.is_authenticated:
        return redirect('test')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=email)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'appadmin/login.html', context)

                 # Check if the user's role is not equal to 1
        if user.role != 2:
            messages.error(request, 'You do not have permission to login')
            return render(request, 'appadmin/login.html', context)
        
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dash')
        else:
            messages.error(request, 'Username OR password does not exit')

    return render(request, 'appadmin/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('loginad')


def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('dash')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'appadmin/login.html', {'form': form})

def test(request):
    return render(request, 'test.html')
def logoutUser(request):
    logout(request)
    return redirect('loginad')


def adminpro(request):
    return render(request,'appadmin/adminpro.html') 

def editC(request):
    return render(request,'appadmin/editC.html')

def reports(request):
    return render(request,'appadmin/reports.html')

def editR(request):
    return render(request,'appadmin/editR.html')

def listecandidat(request):
    return render(request,'appadmin/listecandidat.html')

def listerecruteur(request):
    return render(request,'appadmin/listerecruteur.html')

def dash(request):
  nombre_candidats = User.objects.filter(role=0).count()
  nombre_rec = User.objects.filter(role=1).count()
  nombre_admin = User.objects.filter(role=2).count()


  return render(request,'appadmin/dashadmin.html',{'nombre_candidats':nombre_candidats,'nombre_rec':nombre_rec,'nombre_admin':nombre_admin})
def Admin(request):
    if request.method == 'POST':
        id = request.POST.get('delete_id')
        admin = User.objects.get(id=id)
        current_user = request.user 

        if admin != current_user:  
            admin.delete()

    admins = User.objects.filter(role=2)
    return render(request, 'appadmin/adminpro.html', {'admins': admins})


def listecandidat(request):
    if request.method == 'POST':
        id=request.POST.get('delete_id')
        role_1_users = User.objects.get(id=id)
        role_1_users.delete()
    role_1_users = User.objects.filter(role=1)
    
    return render(request, 'appadmin/listecandidat.html', {'role_1_users': role_1_users})

def listerecruteur(request):
    if request.method == 'POST':
        id=request.POST.get('delete_id')
        role_0_users = User.objects.get(id=id)
        role_0_users.delete()
    role_0_users = User.objects.filter(role=0)
    
    return render(request, 'appadmin/listerecruteur.html', {'role_0_users': role_0_users})


def report_list(request):
    if request.method == 'POST':
        report_id = request.POST.get('delete_id')
        report = get_object_or_404(Report, pk=report_id)
        report.delete()

    reports = Report.objects.all()

    return render(request, 'reports.html', {'reports': reports})



def toggle_user_status(request):
    if request.method == 'POST':
        user_id = request.POST.get('toggle_id')
        action = request.POST.get('action')

        user = User.objects.get(id=user_id)
        if user.role == 0:  
            if action == 'enable':
                user.is_active = True
            elif action == 'disable':
                user.is_active = False

            user.save()

        return HttpResponseRedirect(reverse('listerecruteur'))

    return render(request, 'listerecruteur.html')


def toggle_candidat_status(request):
    if request.method == 'POST':
        candidat_id = request.POST.get('toggle_id')
        action = request.POST.get('action')

        candidat = User.objects.get(id=candidat_id)

        if candidat.role == 1:  
            if action == 'enable':
                candidat.is_active = True
            elif action == 'disable':
                candidat.is_active = False

            candidat.save()

        return HttpResponseRedirect(reverse('listecandidat')) 

    return render(request, 'listecandidat.html')
