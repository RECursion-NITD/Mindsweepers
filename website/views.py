from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from website.models import Profile, StartEvent
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta

class LoginView(APIView):
    def post(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        start = StartEvent.objects.all()[0]
        time_left = timedelta(seconds=1) - (timezone.now() - start.start_time)
        time_left = max(time_left, timedelta(0))
        if(time_left > timedelta(0)):
            return JsonResponse(status=400,data={
				'error': 'Event will start in '+ str(time_left.seconds//3600) + ' hours ' + str((time_left.seconds % 3600)//60) + ' minutes',  
			})
        if(user==None):
            return JsonResponse(data={
                'error': 'Invalid credentials'
            },status=400)
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['phone_number'] = user.profile.phone_number
        refresh['points'] = user.profile.points 
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
        start = StartEvent.objects.all()[0]
        time_left = timedelta(seconds=10800) - (timezone.now() - start.start_time)
        time_left = max(time_left, timedelta(0))
        if(time_left > timedelta(0)):
            return JsonResponse(status=400,data={
				'error': 'Event will start in '+ str(time_left.seconds//3600) + ' hours ' + str((time_left.seconds % 3600)//60) + ' minutes',  
			})
        if( profile_exist ):
            return JsonResponse(data={
                'error': 'Phone number already exists'
            },status=400)
        if( user_exist ):
            return JsonResponse(data={
                'error': 'Username already exists'
            },status=400)
        user = User.objects.create_user(username=username, password=password)
        profile = Profile.objects.create(user=user, phone_number=phone_number)
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['phone_number'] = user.profile.phone_number
        refresh['points'] = user.profile.points
        return JsonResponse(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        },status=201)
    
class FetchRankings(APIView):
    def post(self,request):
        try:
            profiles = Profile.objects.all().order_by('-points').filter(role='3')
        except Profile.DoesNotExist:
            return JsonResponse(status=404,data={'message':'No user exists'})
        
        return JsonResponse(status=200,data={
            'rankings': [
                {
                    'username': profile.user.username,
                    'phone_number': profile.phone_number,
                    'points': profile.points
                } for profile in profiles
            ]
        })