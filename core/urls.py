from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('skills/', views.skills, name='skills'),
    path('projects/', views.projects, name='projects'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact, name='contact'),
]
