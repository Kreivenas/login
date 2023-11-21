from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfile
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import redirect, render, get_object_or_404



def index(request):
    return render(request, 'index.html')


class UserProfileView(APIView):
    def get(self, request, pk):
        user_profile = UserProfile.objects.get(pk=pk)
        return Response(user_profile.to_dict())

    def post(self, request):
        user_profile = UserProfile(
            username=request.data['username'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name'],
            email=request.data['email'],
        )
        user_profile.save()
        return Response(user_profile.to_dict())


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': True})
        else:
            return Response({'success': False})
        

class LogoutView(APIView):
    def get(self, request):
        logout(request)
        return Response({'success': True})    


class RegistrationView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        email = request.data['email']

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )

        login(request, user)
        return Response({'success': True})        