from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects), # wird dann zu /api/projects
    path('projects/<str:pk>', views.getProject),
]