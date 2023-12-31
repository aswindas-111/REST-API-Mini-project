from rest_framework import serializers
from . models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError




class UserRegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(max_length=50,min_length=6,write_only=True)
    password2=serializers.CharField(max_length=50,min_length=6,write_only=True)
    
    class Meta:
        model=User
        fields=['email','first_name','last_name','password','password2']
        
    def validate(self,attrs):
        password=attrs.get('password','')
        password2=attrs.get('password2','')
        if password != password2:
            raise serializers.ValidationError('Password do not match')
        return attrs
    
    
    def create(self,validated_data):
        user=User.objects.create_user(
            email=validated_data['email'],
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            password=validated_data.get('password')
        )
        return user
    
    
    
class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255,min_length=6)
    password=serializers.CharField(max_length=50,write_only=True)
    full_name=serializers.CharField(max_length=255,read_only=True)
    access_token=serializers.CharField(max_length=255,read_only=True)
    refresh_token=serializers.CharField(max_length=255,read_only=True)
    
    class Meta:
        model=User
        fields=['email','password','full_name','access_token','refresh_token']
        
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')
        request=self.context.get('request')
        user=authenticate(request,email=email,password=password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        user_tokens=user.tokens()
        
        return {
            'email':user.email,
            'full_name':user.get_full_name,
            'access_token':str(user_tokens.get('access')),
            'refresh_token':str(user_tokens.get('refresh')),
        } 


class LogoutUserSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    default_error_message = {
        'bad_token':('Token is Expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            # Blacklist the refresh token
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')