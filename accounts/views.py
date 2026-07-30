from django.shortcuts import render
from .serializers import RegisterSerializer, LoginSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer 
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User registered successfully.", 'user': serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            user = data['user']
            tokens = get_tokens_for_user(user)
            return Response(
                {"message": "Login successful.", 
                 "tokens": tokens, 
                 "user": {
                    "email": user.email, 
                    "first_name": user.first_name, 
                    "last_name": user.last_name
                    }
                 }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class ResetPasswordRequestView(APIView):
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.get(email=email)
            otp = user.generate_otp()
            user.email_user(
                subject="Reset Password",
                message=f"{otp}"
            )
            return Response({"message": "OTP sent to this email."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
            
class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            password = serializer.validated_data['password']
            user = CustomUser.objects.get(email=email)
            if user.verify_otp(otp):
                user.set_password(password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'})
            else:
                return Response({"message": "Invalid OTP"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    