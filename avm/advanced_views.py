from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

from serializers import *
from pizdaint import pizdaint

from service_account.settings import ENABLED_HPC as HPC
from service_account.settings import DEFAULT_PROJECT as PROJECT

import json



# To implement permission classes
@csrf_exempt
def pizdaint(request, project_name=None):
    return HttpResponse('CIAONE')
    if not project_name:
        project = DEFAULT_PROJECT['PIZDAINT']
        print project

    if project.hpc != 'PIZDAINT':
        return HttpResponseNotFound

    if request.method == 'POST':
        pass


    elif request.method == 'GET':
        pass


    return HttpResponse()
