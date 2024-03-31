from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from website.models import Profile
from .models import Game
import random as rnd
import json




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


class ValidateStringView(APIView):
	def post(self,request):
		phone_number=request.data.get('phone')
		input_string = request.data.get('input')
		try:
			profile=Profile.objects.get(phone_number=phone_number)
		except Profile.DoesNotExist:
			return JsonResponse(status=404,data={
				'message':'No user exists'
            })
		try:
			game_instance=Game.objects.get(game_user=profile)
		except Game.DoesNotExist:
			print("ok")
			equ=equationGenerate()
			game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], ques_string=equ)
		game_string_arr=game_instance.game_string_arr
		game_string_arr = list(game_string_arr)
		game_string_arr.append(input_string)
		game_string_arr_json = json.dumps(game_string_arr)
		game_instance.game_string_arr=game_string_arr_json
		game_instance.save()
		valid_string=validate(input_string,game_instance.ques_string)
		return JsonResponse(status=200,data={
			'validity':valid_string
        })
			

def validate(input_string, correct_string):
    bool_string = "0" * len(input_string)  # Initialize bool_string with zeros
    correct_list = list(correct_string)   # Convert correct_string to a list for modification

    for i in range(len(input_string)):
        for j in range(len(correct_list)):
            if input_string[i] == correct_list[j]:
                if i == j:
                    bool_string = bool_string[:i] + '1' + bool_string[i+1:]  # Update bool_string at position i
                    correct_list[j] = 'x'  # Mark the character as matched in correct_list
                else:
                    bool_string = bool_string[:i] + '1' + bool_string[i+1:]  # Update bool_string at position i
                    correct_list[j] = 'x'  # Mark the character as matched in correct_list
                break

    return bool_string

			
	

def validate_input_string(input_string, correct_answer):
    return input_string == correct_answer

def check_game_won(is_valid):
    return is_valid


class MathsWordleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        return JsonResponse(status=200,data={
            'message': 'Hello World'
        })

# def randomEquationView(request, user_id):
#     return request
