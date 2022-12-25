from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from api.serializers import UserSerializer, RegisterSerializer, LoginSerializer
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from . import serializers
from rest_framework.permissions import IsAuthenticated

'''
User Registration View
'''
class UserRegisterAPI(APIView):
    # @csrf_exempt
    def get(self, request, format = None):
        user = User.objects.all()
        print(user)
        serializer = UserSerializer(user, many = True) 
        print(serializer)
        return Response(serializer.data,status=status.status.HTTP_200_OK)
    # @csrf_exempt
    def post(self, request, format = None):
        serializer = RegisterSerializer(data = request.data)
        print(serializer)
        if serializer.is_valid(raise_exception=True):
            user =  serializer.save()

            token = Token.objects.create(user=user)
            print(token.key)   
            username = user.username
            print(username)
            return Response({'token': token.key, "message": "You have successfully logged in", "user": username},
                status=status.HTTP_200_OK)
        else:
            return Response({"message" : "user has not been created" }, status=status.HTTP_400_BAD_REQUEST)


'''
User Login View
'''

# class UserLoginAPI(APIView):
    
#     def post(self, request, format = None):
#         serializer = UserLoginSerializer(data = request.data)
#         username = request.data.get("username")
#         password = request.data.get("password")
#         print(username, password, "ppp")
#         if username is None or password is None:
#             return Response({'error': 'Please provide both username and password'},
#                         status=status.HTTP_400_BAD_REQUEST)
#         user = authenticate(username=username, password=password)
        
#         if not user:
#             return Response({'error': 'Invalid Credentials'},
#                 status=status.HTTP_404_NOT_FOUND)
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key, "message": "You have successfully logged in"},
#                     status=status.status.HTTP_200_OK)



# class UserLoginAPI(APIView):
    
#     def post(self, request, format = None):
#         serializer = UserLoginSerializer(data = request.data)
#         # username = request.data.get("username")
#         # password = request.data.get("password")
#         # print(username, password, "ppp")
#         # if username is None or password is None:
#         #     return Response({'error': 'Please provide both username and password'},
#         #                 status=status.HTTP_400_BAD_REQUEST)
#         # user = authenticate(username=username, password=password)
        
#         # if not user:
#         #     return Response({'error': 'Invalid Credentials'},
#         #         status=status.HTTP_404_NOT_FOUND)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.data
#         print(user)
#         token, _ = Token.objects.get_or_create(user=user)
#         return Response({'token': token.key, "message": "You have successfully logged in"},
#                     status=status.status.HTTP_200_OK)

class LoginView(APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, "message": "You have successfully logged in"},
            status=status.HTTP_200_OK)



'''
User Logout View
'''
class UserLogoutAPI(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response('User Logged out successfully')
