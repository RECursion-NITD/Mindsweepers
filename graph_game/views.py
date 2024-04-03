from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import Node

class GraphGameView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def generate_tree(self):
        try:
            Node.objects.all().delete()

            odd_integers = [2 * i + 1 for i in range(7)]

            root = Node.objects.create(value=odd_integers[0])

            for i in range(1, 7):
                node = Node.objects.create(value=odd_integers[i], parent=root)

            return {'success': True, 'message': 'Tree generated successfully'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def validate_tree(self):
        try:
           
            nodes = Node.objects.all()

            if nodes.count() != 7:
                return {'valid': False, 'message': 'Tree must have exactly 7 nodes'}

            visited = set()
            stack = [(nodes[0], None)]  
            while stack:
                node, parent = stack.pop()
                if node in visited:
                    return {'valid': False, 'message': 'Cycle detected in the tree'}
                visited.add(node)
                children = node.children.all()
                for child in children:
                    if child != parent:  
                        stack.append((child, node))

            
            differences = set()
            for node in nodes:
                if node.parent:
                    difference = abs(node.value - node.parent.value)
                    if difference in differences:
                        return {'valid': False, 'message': 'Each edge must have a distinct difference'}
                    differences.add(difference)

            return {'valid': True, 'message': 'Tree is valid'}
        except Exception as e:
            return {'valid': False, 'message': str(e)}

    def post(self, request):
        result = self.generate_tree()
        return JsonResponse(result)

    def get(self, request):
        result = self.validate_tree()
        return JsonResponse(result)
