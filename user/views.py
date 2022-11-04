from urllib import response
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from user.models import UserSerializer, RegisterSerializer, UserAPISerializer
from rest_framework.views import APIView
# from django.contrib.auth import login

# from rest_framework import permissions
# from rest_framework.authtoken.serializers import AuthTokenSerializer
# from knox.views import LoginView as KnoxLoginView
from django.contrib.auth.models import User
# Create your views here.


class UserAPI(APIView):
    def get(self, request, format = None):
        user = User.objects.all()
        print(user)
        serializer = UserSerializer(user, many = True) 
        print(serializer)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request, format = None):
        serializer = RegisterSerializer(data = request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED )



class UserLoginAPI(APIView):
    def post(self, request):
        serializer = UserAPISerializer(data = request.data)
        serializer.is_valid()
        user = serializer.validated_data['user']
        return Response(user.data)


# class LoginView(KnoxLoginView):
#     permission_classes = (permissions.AllowAny,)

#     def post(self, request, format=None):
#         serializer = AuthTokenSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(LoginView, self).post(request, format=None)



