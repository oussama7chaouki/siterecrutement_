from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="loginc"),
    path('logout/', views.logoutUser, name="logoutc"),
    path('register/', views.registerPage, name="registerc"),
    path('apply/<str:pk>', views.apply, name="apply"),
    path('report/<str:pk>', views.report, name="report"),
    path('candidature/', views.candidature, name="candidature"),
    path('delete_candidature/', views.delete_candidature, name='delete_candidature'),
    path('view_score/<int:candidature_id>/', views.view_score, name='view_score'),
    path('Reports/', views.listReport, name="reports"),

    path('compte/', views.compte, name="comptecan"),
    path('profile_form/', views.profile_form, name='profile_form'),
    path('settings/', views.profile_details, name='settingscan'),
    path('cvupload/', views.cvupload, name='cvupload')
]