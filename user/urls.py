from django.urls import path
# from knox.views import LoginView as KnoxLoginView
# from rest_framework import generics, permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.models import AuthToken

from user import views
 
urlpatterns = [
   
    path('signup/', views.UserRegisterAPI.as_view()),
    path('login/', views.UserLoginAPI.as_view())
]    

