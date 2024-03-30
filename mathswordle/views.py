from django.http import JsonResponse
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