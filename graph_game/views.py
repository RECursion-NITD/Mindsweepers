from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
import json
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
    validity = list("1111111")
    edgeDifferences = set()
    for i in range(0, 7):
        for j in range(0, 7):
            if(adjacency_matrix[i][j]):
                if(abs(node_values[i + 1] - node_values[j + 1]) in edgeDifferences):
                    validity[i] = '0'
                    validity[j] = '0'
                edgeDifferences.add(abs(node_values[i + 1] - node_values[j + 1]))

    return validity

class GraphGameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self,request):
        return JsonResponse(status=200,data={
            'Valid': validateTreeFunction(request.data)
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


