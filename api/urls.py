from django.urls import path
from . import views

# simple-jwt
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# simple-jwt ist für sog. refresh-token, die länger als 5 Minuten halten

urlpatterns = [
    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects), # wird dann zu /api/projects
    path('projects/<str:pk>', views.getProject),
]