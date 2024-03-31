from django.http import JsonResponse
sathvika-validation
from django.views import View
from .models import GameState

class ValidateStringView(View):
    def post(self, request, *args, **kwargs):
       
        input_string = request.POST.get('input_string')

     
        game_state = GameState.objects.last()

        
        is_valid = validate_input_string(input_string, game_state.correct_answer)

        
        response_data = {
            'is_valid': is_valid,
            'game_won': check_game_won(is_valid),
        }

        return JsonResponse(response_data)

def validate_input_string(input_string, correct_answer):
    """
    Validates the user's input string against the correct answer.

    Args:
        input_string (str): The user's input string.
        correct_answer (str): The correct answer for the game.

    Returns:
        bool: True if the input string matches the correct answer, False otherwise.
    """
    
    return input_string == correct_answer

def check_game_won(is_valid):
    """
    Determines if the game has been won based on the validity of the user's input string.

    Args:
        is_valid (bool): Whether the user's input string is valid.

    Returns:
        bool: True if the game has been won (input string is valid), False otherwise.
    """
    return is_valid
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from website.models import Profile
from .models import Game
import random as rnd

def convertToString(a):
	if(a < 10):
		return "0" + str(a)
	else:
		return str(a)

def equationGenerate():
	equation = ""
	operations = ["+", "-", "/", "*"]

	firstInteger = 0
	secondInteger = 0
	thirdInteger = 0
	firstIntegerStr = ""
	secondIntegerStr = ""
	thirdIntegerStr = ""
	resStr = ""

	operationSelected = rnd.choice(operations)
	if operationSelected == '+':
		firstInteger = rnd.randrange(1, 100)
		if firstInteger == 99:
			secondInteger = 0
		else:
			secondInteger = rnd.randrange(1, 100 - firstInteger)
	elif operationSelected == '-':
		firstInteger = rnd.randrange(1, 100)
		secondInteger = rnd.randrange(1, firstInteger + 1)
	elif operationSelected == '*':
		firstInteger = rnd.randrange(1, 50)

		if int(100/firstInteger) == 1:
			secondInteger = 1
		else:
			secondInteger = rnd.randrange(1, int(100/firstInteger))
	elif operationSelected == '/':
		secondInteger = rnd.randrange(1, 25)
		if int(100/secondInteger) == 1:
			thirdInteger = 1
		else:
			thirdInteger = rnd.randrange(1, int(100/secondInteger))

		firstInteger = thirdInteger * secondInteger

	if operationSelected == '+':
		thirdInteger = firstInteger + secondInteger
	elif operationSelected == '-':
		thirdInteger = firstInteger - secondInteger
	elif operationSelected == '*':
		thirdInteger = firstInteger * secondInteger

	#third integer is already calculated for division

	firstIntegerStr = convertToString(firstInteger)
	secondIntegerStr = convertToString(secondInteger)
	thirdIntegerStr = convertToString(thirdInteger)

	equation = firstIntegerStr + operationSelected + secondIntegerStr + "=" + thirdIntegerStr
	return equation

class MathsWordleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        return JsonResponse(status=200,data={
            'message': 'Hello World'
        })

def randomEquationView(request, user_id):
    return request
 main
