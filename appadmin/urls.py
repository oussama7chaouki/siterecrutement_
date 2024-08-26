from django.urls import path
from . import views

urlpatterns = [
    
    path('test/', views.test, name="test"),
    path('login/', views.loginPage, name="loginad"),
    path('logout/', views.logoutUser, name="logoutad"),
    path('register/', views.registerPage, name="registerad"),
    path('dash/', views.dash, name="dash"),
    path('adminpro/', views.Admin, name="adminpro"),
    path('editc/', views.editC, name="editc"),
    path('editr/', views.editR, name="editr"),
    path('reports/', views.reports, name="reports"),
    path('listerecruteur/', views.listerecruteur, name="listerecruteur"),
    path('listecandidat/', views.listecandidat, name="listecandidat"),
     path('toggle_user_status/', views.toggle_user_status, name='toggle_user_status'),
      path('toggle_candidat_status/', views.toggle_candidat_status, name='toggle_candidat_status'),
    
]
