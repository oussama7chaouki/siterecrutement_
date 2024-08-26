from django.urls import path
from . import views

urlpatterns = [

    path('getjob/<str:pk>/', views.getJob,name="getjob"),
    path('jobs', views.getJobs,name="jobs"),
    path('job', views.sendJob,name="job"),
    path('accept_candidature', views.accept_candidature,name="accept_candidature"),
    path('reject_candidature', views.reject_candidature,name="reject_candidature"),
    path('fetch', views.fetch_user,name="fetch"),






]