from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from website.models import Profile
from .models import Game
import random as rnd
import json

def operateOnNumbers(firstNumber, secondNumber, operationStr):
	if(operationStr == '+'):
		return firstNumber + secondNumber
	elif(operationStr == '-'):
		return firstNumber - secondNumber
	elif(operationStr == '*'):
		return firstNumber * secondNumber
	elif(operationStr == '/'):
		return firstNumber / secondNumber

def validateString(equationstr):
	operatorList = ['+', '*', '/', '-', '=']

	operatorNum = 0
	equalIndex = -1
	operatorIndex = -1

	firstNumber = 0
	secondNumber = 0
	operatedNumber = 0

	if(len(equationstr) != 8):
			return False
	else:
		for i in range(0, 8):
			found = equationstr[i] in operatorList
			if found:
				operatorNum += 1

			if found and equationstr[i] == '=':
				equalIndex = i
			elif found and equationstr[i] != '=':
				operatorIndex = i

		if(operatorNum != 2):
			return False
		
		try:
			if(operatorIndex < equalIndex):
				firstNumber = int(equationstr[0:operatorIndex])
				secondNumber = int(equationstr[operatorIndex + 1: equalIndex])
				operatedNumber = int(equationstr[equalIndex + 1: 8])
			elif(operatorIndex > equalIndex):
				firstNumber = int(equationstr[operatorIndex + 1 : 8])
				secondNumber = int(equationstr[equalIndex + 1: operatorIndex])
				operatedNumber = int(equationstr[0: equalIndex])

			if(operateOnNumbers(firstNumber, secondNumber, equationstr[operatorIndex]) == operatedNumber):
				return True
			else:
				return False
		except:
			return False

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
			equ=equationGenerate()
			game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], verdict=[], ques_string=equ)
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
            game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], verdict=[], ques_string=equationGenerate())
        game_instance.moves=0
        game_instance.game_string_arr=[]
        game_instance.ques_string=equationGenerate()
        game_instance.verdict=[]
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


