from django.urls import path
from profiles import views

urlpatterns = [
    path('', views.ProfileList.as_view()),  # Handle requests to the root URL
    path('profiles/', views.ProfileList.as_view()),  # List all profiles
    path('profiles/<int:pk>/', views.ProfileDetail.as_view()),  # Retrieve, update or delete a profile
]