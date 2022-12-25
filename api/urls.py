from django.urls import path
from api import views
# from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    
    path('register/', (views.UserRegisterAPI.as_view())),
    path('login/', (views.LoginView.as_view())),
    path('logout/', views.UserLogoutAPI.as_view())
]