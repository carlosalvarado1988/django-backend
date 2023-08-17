import json
from django.http import JsonResponse

def api_home(request, *args, **kwargs):
    body = request.body #byte string of JSON data
    print(request.GET)
    print(body)
    data = {}
    try: 
        data = json.loads(body)
    except:
        pass
    print(data)
    data['params'] = dict(request.GET)
    data['headers'] = dict(request.headers)
    data['content_type'] = request.content_type
    return JsonResponse(data)