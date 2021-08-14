from django.shortcuts import redirect

def index(request):
    response = redirect('/api/menus/')
    return response

