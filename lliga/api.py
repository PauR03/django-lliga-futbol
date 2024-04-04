from django.http import JsonResponse
from .models import *
    
#...
    
def get_lligues(request):
    jsonData = list( Lliga.objects.all().values() )
    return JsonResponse({
            "status": "OK",
            "lligues": jsonData,
        }, safe=False)

