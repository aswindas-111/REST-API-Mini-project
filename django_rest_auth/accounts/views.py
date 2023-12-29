from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from . serializers import UserRegisterSerializer, LoginSerializer, LogoutUserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from . utils import send_code_to_user
from . models import OneTimePassword
from django.contrib.auth import logout
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed

# Create your views here.


class RegisterUserView(GenericAPIView):
    serializer_class=UserRegisterSerializer
    
    def post(self,request):
        user_data=request.data
        serializer=self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user=serializer.data
            send_code_to_user(user['email'])
            # send email function user['email]
            print(user)
            return Response({
                'data':user,
                'message':f'hi {user["first_name"]} thanks for signing up, a code is send to your mail id',
            },status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            
            

class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otpcode=request.data.get('otp')
        try:
            user_code_obj= OneTimePassword.objects.get(code=otpcode)
            user = user_code_obj.user
            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({'message':'email is verified'},status=status.HTTP_200_OK)
            return Response({'message':'code is invalid, user already verified'},status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist:
            return Response({'message':'passcode not provided'},status=status.HTTP_404_NOT_FOUND)
        
        

class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            raise AuthenticationFailed('Email and password are required.')

        user = authenticate(request, email=email, password=password)

        if user:
            if user.is_verified:
                user_tokens = user.tokens()
                access_token = str(user_tokens.get('access'))
                refresh_token = str(user_tokens.get('refresh'))

                return Response({
                    'email': user.email,
                    'full_name': user.get_full_name,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                }, status=status.HTTP_200_OK)
            else:
                # Return a response indicating that the email is not verified
                return Response({"message": "Email not verified. Please verify your email before login."},status=status.HTTP_403_FORBIDDEN)
        else:
            raise AuthenticationFailed('Invalid email or password.')
    



class LogoutUserView(GenericAPIView):
    serializer_class=LogoutUserSerializer
    permission_classes=[IsAuthenticated]
    
    def post(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'message': 'Logout successfully'},status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'message': 'User is already logged out'}, status=status.HTTP_200_OK)
    



# class TestAuthenticationView(GenericAPIView):
#     permission_classes=[IsAuthenticated]
    
#     def get(self,request):
#         data={
#             'msg':'its works'
#         }
#         return Response(data,status=status.HTTP_200_OK)
    