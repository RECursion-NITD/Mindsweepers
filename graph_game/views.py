from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from website.models import Profile
from .models import GraphGame
import json
import random
from django.utils import timezone
from datetime import datetime, timedelta
 
def generate_random_tree(n):
    length = n
    nodeContainer = []
    treeContainer = [1]
    edgeContainer = []
    for i in range(2, length+1):
        nodeContainer.append(i)
    for i in range(2, length+1):
        sel_node = random.choice(treeContainer)
        get_node = random.choice(nodeContainer)
        nodeContainer.remove(get_node)
        treeContainer.append(get_node)
        edgeContainer.append([sel_node, get_node])
        treeContainer.append(sel_node)

    # add more edges
    # edge_number = random.randint(0, 7)
    # for i in range(0, edge_number):
    #     sel_node = random.choice(treeContainer)
    #     get_node = random.choice(treeContainer)
    #     if [sel_node, get_node] in edgeContainer or [get_node, sel_node] in edgeContainer or sel_node == get_node:
    #         i -= 1
    #         continue
    #     edgeContainer.append([sel_node, get_node])

    return edgeContainer
        

def formattedTree():
    edgeContainer = generate_random_tree(7)
    listOfEdgesOfUI = []
    idx = 1
    for tup in edgeContainer:
        formatted_string = { "source": str(tup[0]), "target": str(tup[1]), "value": str(idx) }
        listOfEdgesOfUI.append(formatted_string)
        idx += 1
    #final_string = ",\n".join(listOfEdgesOfUI)
    return listOfEdgesOfUI

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

def process_graph_data(data):
    #data = json.loads(json_string)
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

def validateTreeFunction(data):
    adjacency_matrix, node_values = process_graph_data(data)
    validity = list("0000000")
    edge_validity = list("0"*len(data.get('links',[])))
    edgeDifferences = [-1]*15
    node_set = [-1]*15
    for i in range(0, 7):
        if node_values[i + 1] > 13 or node_values[i + 1] <= 0 or node_values[i + 1] % 2 == 0:
            validity[i] = '1'
        if node_set[node_values[i + 1]] == -1:
            node_set[node_values[i + 1]] = i
        else:
            validity[i] = '1'
            validity[node_set[node_values[i + 1]]] = '1'
    links = data.get('links', [])
    for i in range(0, len(links)):
        source = int(links[i]['source'])
        target = int(links[i]['target'])
        if edgeDifferences[abs(node_values[source] - node_values[target])] == -1:
            edgeDifferences[abs(node_values[source] - node_values[target])] = i
        else:
            edge_validity[edgeDifferences[abs(node_values[source] - node_values[target])]] = '1'
            edge_validity[i] = '1'

    return validity, edge_validity

class GraphGameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        user = request.user
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            return JsonResponse(status=404, data={'message': 'No user exists'})
        try:
            game_instance = GraphGame.objects.get(game_user=profile)
        except GraphGame.DoesNotExist:
            return JsonResponse(status=404, data={'message': 'No game exists'})
        game_instance.tree_structure = request.data
        game_instance.save()
        verdict = 0
        validate, edge_validate = validateTreeFunction(request.data)
        if validate == list("0000000") and edge_validate == list("0"*len(request.data.get('links',[]))):
            verdict = 1
            profile.points += 5
            profile.save()
        return JsonResponse(status=200,data={
            'validate': validate,
            'edgeValidate': edge_validate,
            'verdict': verdict
        })
    
class GraphGenerateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        return JsonResponse(status=200,data={
            "nodes" : [{ "id": "1", "group": "team1", "value": "0"},
                          { "id": "2", "group": "team2", "value": "0"},
                          { "id": "3", "group": "team3", "value": "0"},
                          { "id": "4", "group": "team4", "value": "0"},
                          { "id": "5", "group": "team4", "value": "0"},
                          { "id": "6", "group": "team4", "value": "0"},
                          { "id": "7", "group": "team4", "value": "0"}
                          ],
            'links': formattedTree()
        })
    
class CreateGraphGameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone_number = request.data.get('phone')
        
        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            return JsonResponse(status=404, data={'message': 'No user exists'})
        
        try:
            game_instance = GraphGame.objects.get(game_user=profile)
        except GraphGame.DoesNotExist:
            game_instance = GraphGame.objects.create(
                game_user=profile,
                tree_structure={
                    "nodes" : [{ "id": "1", "group": "team1", "value": "0"},
                        { "id": "2", "group": "team2", "value": "0"},
                        { "id": "3", "group": "team3", "value": "0"},
                        { "id": "4", "group": "team4", "value": "0"},
                        { "id": "5", "group": "team4", "value": "0"},
                        { "id": "6", "group": "team4", "value": "0"},
                        { "id": "7", "group": "team4", "value": "0"}
                    ],
                    'links': formattedTree()
                },
                last_reset_time = timezone.now()
            )
        time_left = timedelta(seconds=60) - (timezone.now() - game_instance.last_reset_time)
        time_left = max(time_left, timedelta(0))
        if(time_left > timedelta(0) and game_instance.moves < 6):
            return JsonResponse(status=200,data={
				'message': 'wait for '+ str(time_left.seconds) + ' seconds',
			})
        game_instance.tree_structure = {
            "nodes" : [
                { "id": "1", "group": "team1", "value": "0"},
                { "id": "2", "group": "team2", "value": "0"},
                { "id": "3", "group": "team3", "value": "0"},
                { "id": "4", "group": "team4", "value": "0"},
                { "id": "5", "group": "team4", "value": "0"},
                { "id": "6", "group": "team4", "value": "0"},
                { "id": "7", "group": "team4", "value": "0"}
            ],
            'links': formattedTree()
        }
        game_instance.moves = 0 
        game_instance.last_reset_time = timezone.now() 
        game_instance.save()  

        return JsonResponse(status=200, data={'message': 'Done'})
    

class GetGraphView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        phone_number = request.data.get('phone')
        try:
            profile = Profile.objects.get(phone_number=phone_number)
        except Profile.DoesNotExist:
            return JsonResponse(status=404, data={'message': 'No user exists'})
        
        try:
            game_instance = GraphGame.objects.get(game_user=profile)
        except GraphGame.DoesNotExist:
            game_instance = GraphGame.objects.create(
                game_user=profile,
                tree_structure={
                    "nodes" : [{ "id": "1", "group": "team1", "value": "0"},
                        { "id": "2", "group": "team2", "value": "0"},
                        { "id": "3", "group": "team3", "value": "0"},
                        { "id": "4", "group": "team4", "value": "0"},
                        { "id": "5", "group": "team4", "value": "0"},
                        { "id": "6", "group": "team4", "value": "0"},
                        { "id": "7", "group": "team4", "value": "0"}
                    ],
                    'links': formattedTree()
                }
            )

        return JsonResponse(status=200, data=game_instance.tree_structure)

