from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from website.models import Profile
from .models import Game
import random as rnd
import math
import json
from django.utils import timezone
from datetime import datetime, timedelta

def validateString(inputString):
	operations = ['+', '*', '/', '-']
	if(len(inputString) != 8):
		return False
	input = inputString.split('=')
	if(len(input) != 2):
		return False
	lhs = 0
	rhs = 0
	if(input[0].isdigit()):
		lhs = int(input[0])
	else:
		try:
			lhs = eval(input[0])
		except:
			return False
	if(input[1].isdigit()):
		rhs = int(input[1])
	else:
		try:
			rhs = eval(input[1])
		except:
			return False
	if(lhs == rhs):
		return True
	else:
		return False


def convertToString(a):
	if(a < 10):
		return "0" + str(a)
	else:
		return str(a)

def get_upper(num, op):
	if(op == '+'):
		return 99 - num
	elif(op == '-'):
		return num
	elif(op == '*'):
		return 999//num
	else:
		return num

def factors(num):
	fact = []
	for i in range(1, int(math.sqrt(num))+1):
		if(num % i == 0):
			fact.append(i)
			if(num//i != i):
				fact.append(num//i)
	return fact

def generation():
	operations = ['+', '*', '/', '-']
	length = 7
	equation = ""
	op = operations[rnd.randint(0, 3)]
	if(op == '/'):
		num = rnd.randint(100, 1000)
		fact = factors(num)
		while len(fact) == 2:
			num = rnd.randint(1, 1000)
			fact = factors(num)
		num2 = fact[rnd.randint(0, len(fact)-1)]
		equation = str(num) + op + str(int(num2))
	elif(op == '*'):
		num = rnd.randint(1, 100)
		num_length = rnd.randint(1, 2)
		upper = 9
		if(num_length == 2):
			upper = 99//num
		num2 = rnd.randint(1, upper)
		equation = str(num) + op + str(num2)
	elif(op == '+'):
		num = rnd.randint(1, 89)
		lower = 10
		upper = 100-num
		if(num < 10):
			lower = 100-num
			upper = 100
		num2 = rnd.randint(lower, upper)
		equation = str(num) + op + str(num2)
	else:
		upper = rnd.choice([100, 108])
		lower = 20
		if upper == 108:
			lower = 101
		num = rnd.randint(lower, upper)
		num2 = 0
		if(num < 100):
			num2 = rnd.randint(10, num-10)
		else:
			num_length = rnd.randint(1, 2)
			if(num_length == 1):
				num2 = rnd.randint(num-100,10)
			else:
				num2 = rnd.randint(num-10, num)
		equation = str(num) + op + str(num2)
	result = eval(equation)
	equation += '=' + str(int(result))
	return equation

def equationGenerate():
	equation = generation()
	while len(equation) != 8:
		equation = generation()	
		print(equation)
	return equation

class ValidateStringView(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
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
			equ = equationGenerate()
			game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], verdict=[], ques_string=equ, last_reset_time = timezone.now())
		if(game_instance.moves>=6):
			return JsonResponse(status=200,data={
				'validity':'00000000',
				'verdict': 1,
				'message': "moves exceeded"
			})
		
		if(not(validateString(input_string))):
			return JsonResponse(status = 200, data = {
				'verdict' : -1,
				'message' : 'Invalid Input',
				'validity' : '00000000'
			})
		game_instance.game_string_arr.append(input_string)
		game_instance.moves+=1
		valid_string=validate(input_string,game_instance.ques_string)
		game_instance.verdict.append(valid_string)
		game_instance.save()
		verdict=check_game_won(valid_string,game_instance)
		if(verdict==2):
			profile.points+=5
			game_instance.moves=6
			game_instance.save()
			profile.save()
		return JsonResponse(status=200,data={
			'validity':valid_string,
			'verdict': verdict,
			'message': 'ok'
        })
			

def validate(input_string, correct_string):
    bool_string = "0" * len(input_string)  # Initialize bool_string with zeros
    correct_list = list(correct_string)   # Convert correct_string to a list for modification
    print(correct_list)
    for i in range(len(input_string)):
        if input_string[i] == correct_list[i]:
            bool_string = bool_string[:i] + '2' + bool_string[i+1:]  # Update bool_string at position i
            correct_list[i] = 'x'  # Mark the character as matched in correct_list
            input_string = input_string[:i] + 'y' + input_string[i+1:]

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

def check_game_won(valid_string, game_instance):
	verdict = 0 # continue
	if valid_string == "2" * 8:
		verdict = 2 # win
	elif game_instance.moves == 6:
		verdict = 1	# lose
	return verdict


class CreateMathsWordleView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        phone_number=request.data.get('phone')
        try:
            profile=Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            return JsonResponse(status=404,data={
				'message':'No user exists'
			})
        
        try:
            game_instance=Game.objects.get(game_user=profile)
        except Game.DoesNotExist:
            game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], verdict=[], ques_string=equationGenerate(), last_reset_time = timezone.now())
            return JsonResponse(status=200,data={
            	'message': 'done'
        	}) 
        time_left = timedelta(seconds=60) - (timezone.now() - game_instance.last_reset_time)
        time_left = max(time_left, timedelta(0))
        if(time_left > timedelta(0) and game_instance.moves < 6):
            return JsonResponse(status=200,data={
				'message': 'wait for '+ str(time_left.seconds) + ' seconds',
			})

        game_instance.moves=0
        game_instance.game_string_arr=[]
        game_instance.ques_string=equationGenerate()
        game_instance.verdict=[]
        game_instance.last_reset_time = timezone.now()
        game_instance.save() # reset game instance
        return JsonResponse(status=200,data={
            'message': 'done'
        })

class CreateGameState(APIView):
	authentication_classes = [JWTAuthentication]
	permission_classes = [IsAuthenticated]
	def post(self,request):
		phone_number=request.data.get('phone')
		try:
			profile=Profile.objects.get(phone_number=phone_number)
		except Profile.DoesNotExist:
			return JsonResponse(status=404,data={
				'message':'No user exists'
			})
		try:
			game_instance=Game.objects.get(game_user=profile)
		except Game.DoesNotExist:
			game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], verdict=[], ques_string=equationGenerate())
		string_array = [] 
		for i in game_instance.game_string_arr:
			string_array.append(list(i))
		if len(string_array) < 6:
			for i in range(6 - len(string_array)):
				string_array.append(['', '', '', '', '', '', '', ''])
		verdict_array = []
		for i in game_instance.verdict:
			verdict_array.append(list(i))
		if len(verdict_array) < 6:
			verdict_array.append(['-1', '-1', '-1', '-1', '-1', '-1', '-1', '-1'])
			for i in range(6 - len(verdict_array)):
				verdict_array.append(['0', '0', '0', '0', '0', '0', '0', '0'])
		return JsonResponse(status=200,data={
			'stringArray': string_array,
			'moves' : game_instance.moves,
			'verdictArray': verdict_array,
		})


