from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import status


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

    # def create(self, validated_data):
    #     return super().create(validated_data)


# class UserLoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('id', 'username', 'password')
#         # extra_kwargs = {
#         #     "username" : {"write only" : True, "required" : True},
#         #     "password": {"write_only": True, "required" : True}
#         #     }


        
#         def validate(self,  validate_Data):

#             username = validate_Data.get("username")
#             password = validate_Data.get("password")
#             print(username, password, "ppp")
#             if username is None or password is None:
#                 return Response({'error': 'Please provide both username and password'},
#                             status=status.HTTP_400_BAD_REQUEST)
#             user = authenticate(username=username, password=password)
            
#             if not user:
#                 return Response({'error': 'Invalid Credentials'},
#                     status=status.HTTP_404_NOT_FOUND)

#             return user        

#         # def validate(self, instanse, attrs):
#         #     if instanse['password'] != attrs['password']:
#         #         raise serializers.ValidationError(
#         #             {"password": "Password fields didn't match."})
#         #     return attrs



from django.contrib.auth import authenticate

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    username = serializers.CharField(
        label="Username",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs