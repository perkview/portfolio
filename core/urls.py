from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('projects/', views.projects, name='projects'),
    path('contact/', views.contact, name='contact'),
    path('services/', views.services, name='services'),
    path('freelance/', views.hire, name='freelance'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('case-studies/', views.case_studies, name='case_studies'),
    path('case-studies/<slug:slug>/', views.case_study_detail, name='case_study_detail'),


    # to be fixed:
    path('resume/', views.about, name='resume'),
]
