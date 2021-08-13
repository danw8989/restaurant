from django.http import JsonResponse

def getRoutes(request):
    routes = [
        {
            'Endpoint': '/menus/',
            'method': 'GET',
            'body': None,
            'description': 'Return list of menus'
        }
    ]
    return JsonResponse(routes, safe=False)