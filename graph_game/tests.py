from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import GraphGame
from website.models import Profile
import json


class CreateGraphGameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data('phone')
        
        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            return JsonResponse(status=404, data={'message': 'No user exists'})
        
        try:
            game_instance = GraphGame.objects.get(game_user=profile)
        except GraphGame.DoesNotExist:
            game_instance = GraphGame.objects.create(
                game_user=profile,
                tree_structure=json.loads(formattedTree()) 
            )

        
        
        game_instance.tree_structure = json.loads(formattedTree()) 
        game_instance.moves = 0  
        game_instance.save()  

        return JsonResponse(status=200, data={'message': 'Game initialized'})
