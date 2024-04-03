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

import random
 
def print_tree_edges(prufer, m):
    edgeContainer = []
    vertices = m + 2
    vertex_set = [0] * vertices
 
    for i in range(vertices):
        vertex_set[i] = 0
 
    for i in range(vertices - 2):
        vertex_set[prufer[i] - 1] += 1

    j = 0
 
    for i in range(vertices - 2):
        for j in range(vertices):
            if vertex_set[j] == 0:
                vertex_set[j] = -1

                edgeContainer.append((j + 1, prufer[i]))
                vertex_set[prufer[i] - 1] -= 1
 
                break
 
    j = 0

    edgeTuple = []
    for i in range(vertices):
        if vertex_set[i] == 0 and j == 0:
            edgeTuple.append(i + 1)
            j += 1
        elif vertex_set[i] == 0 and j == 1:
            edgeTuple.append(i + 1)

    edgeContainer.append(tuple(edgeTuple))
    return edgeContainer

def generate_random_tree(n):
    length = n - 2
    arr = [0] * length
 
    for i in range(length):
        arr[i] = random.randint(1, length + 1)
 
    setOfEdges = print_tree_edges(arr, length)
    return setOfEdges

def formattedTree():
    edgeContainer = generate_random_tree(7)
    listOfEdgesOfUI = []
    for tup in edgeContainer:
        formatted_string = "{{ source: '{}', target: '{}', value: 1 }}".format(tup[0], tup[1])
        listOfEdgesOfUI.append(formatted_string)

    final_string = ",\n".join(listOfEdgesOfUI)
    return '[' + final_string + ']'

import json

#dummy
json_string = """
    {
    "nodes": [
        { "id": "1", "group": "team1", "value": "0"},
        { "id": "2", "group": "team2", "value": "3"},
        { "id": "3", "group": "team3", "value": "0"},
        { "id": "4", "group": "team4", "value": "0"},
        { "id": "5", "group": "team4", "value": "4"},
        { "id": "6", "group": "team4", "value": "6"},
        { "id": "7", "group": "team4", "value": "0"}
    ],
    "links": [
        { "source": "2", "target": "1", "value": 1 },
        { "source": "3", "target": "2", "value": 1 },
        { "source": "4", "target": "1", "value": 1 },
        { "source": "4", "target": "6", "value": 1 },
        { "source": "7", "target": "3", "value": 1 },
        { "source": "7", "target": "5", "value": 1 },
        { "source": "7", "target": "4", "value": 1 }
    ]
    }
    """

def process_graph_data(json_string):
    data = json.loads(json_string)
    nodes = data.get('nodes', [])
    links = data.get('links', [])

    adjacency_matrix = [[0] * len(nodes) for _ in range(len(nodes))]
    node_values = {}

    for node in nodes:
        node_id = int(node['id'])
        node_value = int(node['value'])
        node_values[node_id] = node_value

    for link in links:
        source = int(link['source'])
        target = int(link['target'])
        adjacency_matrix[source - 1][target - 1] = 1  

    return adjacency_matrix, node_values

def validateTreeFunction():
    adjacency_matrix, node_values = process_graph_data(json_string)

    edgeDifferences = set()
    for i in range(0, 7):
        for j in range(0, 7):
            if(adjacency_matrix[i][j]):
                edgeDifferences.add(abs(node_values[i + 1] - node_values[j + 1]))


    print(len(edgeDifferences))

    if(len(edgeDifferences) != 7):
        return False
    else:
        return True

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
			game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], ques_string=equ)
		if(game_instance.moves>=6):
			return JsonResponse(status=200,data={
				'validity':'00000000',
				'verdict': 1
			})
		
		if(not(validateString(input_string))):
			return JsonResponse(status = 200, data = {
				'verdict' : 0,
				'message' : 'Invalid String'
			})
	
		game_string_arr=game_instance.game_string_arr
		game_string_arr = list(game_string_arr)
		game_string_arr.append(input_string)
		game_string_arr_json = json.dumps(game_string_arr)
		game_instance.game_string_arr=game_string_arr_json
		game_instance.moves+=1
		game_instance.save()
		valid_string=validate(input_string,game_instance.ques_string)
		verdict=check_game_won(valid_string,game_instance)
		if(verdict==2):
			profile.points+=5
			game_instance.moves=6
			game_instance.save()
			profile.save()
		return JsonResponse(status=200,data={
			'validity':valid_string,
			'verdict': verdict
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
            game_instance = Game.objects.create(game_user=profile, moves=0, game_string_arr=[], ques_string=equationGenerate())
        game_instance.moves=0
        game_instance.game_string_arr=[]
        game_instance.ques_string=equationGenerate()
        game_instance.save() # reset game instance
        return JsonResponse(status=200,data={
            'message': 'done'
        })


