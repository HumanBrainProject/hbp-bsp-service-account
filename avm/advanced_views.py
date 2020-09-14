from django.shortcuts import render
from django.http import *
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response

from avm.models import *
from avm.serializers import *
from pizdaint.pizdaint import advance_endpoint as pizdaint, extract_job_data 
from pizdaint.utils.api import ROOT_URL as ORIGINAL_URL
from avm.utils.misc import get_user, update_job_status_and_quota, dump_job
from service_account.settings import ENABLED_HPC as HPC
from service_account.settings import DEFAULT_PROJECT as PROJECT

import requests
import json
import pprint
import re


# NEW_URL = 'https://bspsa.cineca.it/advanced/pizdaint/rest/core'
NEW_URL = 'https://bspsa.cineca.it/advanced/pizdaint'


# To implement permission classes
def user_has_permission(user, project):
    user_groups = user.groups.split(',')
    user_banned_groups = user.banned_from.split(',')
    if user_groups == '':
        return False
    if str(project.id) in user_groups and str(project.id) not in user_banned_groups:
        return True
    return False



def submit_job(user, project, request, headers):
    
    payload = request.POST
    if len(payload) <= 0 and len(request.body) > 0:
        try:
            payload = json.loads(request.body)
        except ValueError:
            payload = request.body
    
    # force job to be submitted on the Service Account's project
    payload['Resources'].update({u'Project': u'ich011'})
    
    # check if user has enough quota
    try:
        runtime = payload['Resources']['Runtime'] 
    except ValueError:
        v = re.findall(r'[0-9]+', payload['Resources']['Runtime'])
        t = re.findall(r'[a-z]+', payload['Resources']['Runtime'])
        if t[0] == 'min':
            runtime = v * 60
        elif t[0] == 'h':
            runtime = v * 60 * 60
        elif t[0] == 'd':
            runtime = v * 60 * 60 * 24
       
    # check for job imports
    if 'Imports' in payload.keys():
        for i in payload['Imports']:
            for k in i.keys():
                i[k] = i[k].replace(NEW_URL, ORIGINAL_URL)

    # check for user's quota
    try:
        quota = Quota.objects.get(user=user, project=project)
    except Quota.DoesNotExist:
        return HttpResponseForbidden('User has not quota!')

    try:
        quota.sub(time=runtime)
    except ValueError:
        update_job_status_and_quota(user=user, project=project)
        try:
            quota.sub(time=runtime)
        except ValueError:
           return HttpResponseForbidden('Quota not enough!')
    
    # check for job title
    try:
        title = payload['Name']
    except KeyError:
        title = None
        

    # adding userid tag before submit job
    k = payload.keys()
    if 'Tags' in k:
        payload['Tags'].append('userid' + user.id)
    elif 'tags' in k:
        payload['tags'].append('userid' + user.id)
    elif 'TAGS' in k:
        payload['TAGS'].append('userid' + user.id)
    else:
        payload.update({'Tags': ['userid' + user.id]})

    print(payload)
    # submit job
    r = pizdaint(method=request.method, append_url='/rest/core/jobs', headers=headers, json=payload)
    if r.status_code == 201:
        # record job
        job_id = r.headers['Location'].split('jobs/')[1].upper()
        r_job = pizdaint(method='GET', url=r.headers['Location'], headers=headers)
        
        data = {
            'title': title,
            'job_id': job_id, 
            'owner': user.id,
            'runtime': float(runtime) / 3600,
            'is_advanced': True,
            'project': project.id,
            'init_date': r_job.json()['submissionTime'],
            'stage': r_job.json()['status']
        }
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
        else:
            print('Serialization error on Advanced pizdaint.')
            print(serializer.errors) 
            print('Job: ')
            pprint.pprint(data)

    return r


@csrf_exempt
def unicore_pizdaint(request, project_name=None):

    # check if user exists
    print(request)
    pprint.pprint(request.META)
    user = get_user(request)
    if not isinstance(user, User):
        return HttpResponseForbidden(user)
  
    # check if project exists
    if not project_name:
        project_name = PROJECT['PIZDAINT']
    try:
        project = Project.objects.get(name=project_name, hpc='PIZDAINT')
    except Project.DoesNotExist:
        return HttpResponseNotFound('Project not found!')

    # check if user has permission
    if not user_has_permission(user, project):
        return HttpResponseForbidden('User has not access or is banned from this project.')

    URL = request.path.split('advanced/pizdaint')[1]

    headers = {}
    if 'HTTP_CONTENT_TYPE' in request.META:
        headers.update({'content-type': request.META['HTTP_CONTENT_TYPE']})
    if 'HTTP_ACCEPT' in request.META:
        headers.update({'accept': request.META['HTTP_ACCEPT']})
    
    if URL == '/rest/core/jobs' and request.method == 'POST':
        r = submit_job(user, project, request, headers)
    
    else:
        json_data = None
        str_data = None
        
        if request.method == 'GET':
            json_data = request.GET
            if json_data:
                URL += '?'
                for k in json_data:
                    URL += k + '=' + str(json_data[k])
            # Add user tag in GET request
            s = URL.split('?tags=')
            try:
                URL = s[0] + '?tags=' + s[1] + ',userid' + user.id
            except IndexError:
                URL = s[0] + '?tags=userid' + user.id

        elif request.method == 'POST':
            json_data = request.POST

        if not json_data:
            try:
                json_data = json.loads(request.body)
            except ValueError:
                str_data = request.body

        r = pizdaint(method=request.method, append_url=URL, headers=headers, data=str_data, json=json_data)
        #print(request.method, r.status_code, r.content, sep='\n')        
        
        if r.status_code == 200:
            if request.method == 'GET' and '/rest/core/jobs/' in URL:
                # update job record if user request job's info
                job_id = URL.split('/rest/core/jobs/')[1].upper()
                try:
                    job = Job.objects.get(job_id=job_id, project=project.id)
                    data = extract_job_data(job, r)
                    serializer = JobSerializer(instance=job, data=data, partial=True)
                    if serializer.is_valid():
                        job = serializer.save()
                        # restore unused quota
                        if job.end_date:
                            delta_time = job.end_date - job.init_date
                            delta_seconds = delta_time.days * 24 * 60 * 60 + delta_time.seconds
                            quota = Quota.objects.get(user=user, project=job.project)
                            quota.add(time=delta_seconds)
                    else:
                        print('Serializer error on Adavanced Job record update')
                        print(serializer.errors)
                        print('Data:')
                        pprint.pprint(job)
                        
                except Job.DoesNotExist:
                    print('Job ' + str(job_id) + ' not exists')

    access_control_expose_headers = []
    response = HttpResponse()
    response.status_code = r.status_code
    
    try:
        new_content = str(r.content.decode('utf-8')).replace(ORIGINAL_URL, NEW_URL)
    except UnicodeDecodeError:
        new_content = r.content

    response.content = new_content
    for k in r.headers.keys():
        if k == 'Content-Length':
            response[k] = len(response.content)
            continue
        elif k == 'Location' or k == 'Content-Type' or k == 'Cache-Control' or k == 'Content-Language' or k == 'Expires' or k == 'Last-Modified' or k == 'Pragma':
            access_control_expose_headers.append(k)

        response[k] = str(r.headers[k]).replace(ORIGINAL_URL, NEW_URL) 
    
    response['Access-Control-Expose-Headers'] = ', '.join(access_control_expose_headers)

    return response

