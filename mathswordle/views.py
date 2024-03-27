from django.http import JsonResponse
from rest_framework.views import APIView

class MathsWordleView(APIView):
    def post(self,request):
        return JsonResponse(status=200,data={
            'message': 'Hello World'
        })

