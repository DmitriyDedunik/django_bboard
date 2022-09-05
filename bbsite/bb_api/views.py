import re
from django.shortcuts import render
from bboard.models import Bb
from django.http import JsonResponse
import json
import requests
from django.views.decorators.csrf import csrf_exempt
 

def list_bb(request):
    bbs = list(Bb.objects.all().values())
    return JsonResponse(bbs, safe=False, json_dumps_params={'indent':4})


def json_test(request):
    
    template = 'json_test.html'
    a = "{'id': '5', 'content': 'lg'}"
    b = "{'id': '52', 'content': 'lg2'}"
    
    response = requests.post('http://127.0.0.1:8000/api/V1/json_test2?text_json='+a, json=b)

    return render(request, template, {'r': response.json()})


@csrf_exempt
def json_test2(request):
    
    answer = {'a': request.GET['text_json'], 'b': request.body.decode('utf8').replace("'", '"')}

    return JsonResponse(answer, safe=False, json_dumps_params={'indent':4})

