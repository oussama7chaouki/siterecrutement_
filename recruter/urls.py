from django.urls import path
from . import views

urlpatterns = [

    path('offer', views.offer,name="offer"),
    path('jobcans', views.jobcans,name="jobcans"),
    path('jobcan/<str:pk>/', views.jobcan,name="jobcan"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('settings/', views.company_details, name="settingscom"),
    path('modify/', views.update_details, name="updatecom"),
    path('create_thread/', views.create_thread, name='create_thread'),
        path('', views.offer,name="default"),

]