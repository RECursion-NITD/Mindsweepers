from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from website.models import Profile
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        refresh = RefreshToken.for_user(user)
        return JsonResponse(status=200,data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

class RegisterView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        phone_number = request.data.get('phone_number')
        profile_exist = Profile.objects.filter(phone_number=phone_number)
        user_exist = User.objects.filter(username=username)
        if( profile_exist ):
            return JsonResponse({
                'error': 'Phone number already exists'
            },status=400)
        if( user_exist ):
            return JsonResponse({
                'error': 'Username already exists'
            },status=400)
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, phone_number=phone_number)
        refresh = RefreshToken.for_user(user)
        return JsonResponse({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },status=201)
    