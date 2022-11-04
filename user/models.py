from dataclasses import fields
from pyexpat import model
from django.db import models
from rest_framework import serializers
from django.contrib.auth.models import User


# Create your models here.

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs =  {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user   



class UserAPISerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')        

