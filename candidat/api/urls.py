from django.urls import path
from . import views

urlpatterns = [


    path('create_formation', views.create_formation, name='create_formation'),
    path('update_formation/<str:formation_id>/', views.update_formation, name='update_formation'),
    path('get_formation/<str:formation_id>/', views.get_formation, name='get_formation'),
    path('delete_formation/<str:formation_id>/', views.delete_formation, name='delete_formation'),
    path('save_language', views.save_language, name='save_language'),
    path('create_experiences', views.create_experience, name='create_experience'),
    path('update_experiences/<str:experience_id>/', views.update_experience, name='update_experience'),
    path('get_experiences/<str:experience_id>/', views.get_experience, name='get_experience'),
    path('delete_experiences/<str:experience_id>/', views.delete_experience, name='delete_experience'),
    path('save_skill', views.save_skill, name='save_skill'),



]