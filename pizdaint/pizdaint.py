from utils.params import *
from utils import api
from datetime import timedelta
from bs4 import BeautifulSoup

import re
import requests
import json


def get_job_id(job_url):
    return job_url.split('jobs/')[1].upper()


def get_job_status(job, headers={}, user_token=None):
    log = ''
    r = api.get_job_status(job_id=job.job_id.lower(), headers=headers, user_token=user_token)
    data = r.content
    
    if r.status_code == 200:
        for l in r.json()['log']:
            log += l + ';'

        end_date = None
        runtime = re.findall('Total: \d+', log)
        if len(runtime) == 1:
            runtime = float(runtime[0].split('Total: ')[1]) + 1.0
            end_date = job.init_date + timedelta(seconds=runtime)

        failed = re.findall('Result: \w+', log)
        if len(failed) == 1:
            failed = failed[0].split('Result: ')[1]

        match = re.findall('Status set to \w+', log)
        if len(match) == 1:
            terminal_stage = True if match[0].split('Status set to ')[1] == 'DONE' else False
        elif len(match) > 1:
            terminal_stage = True if match[-1].split('Status set to ')[1] == 'DONE' else False

        match = re.findall('Processing failed, aborting', log)
        if len(match) >= 1:
            terminal_stage = True

        data = {
            'stage': r.json()['status'],
            'failed': False if failed == 'Success' else True,
            'terminal_stage': terminal_stage
        }

        if end_date:
            data.update({'end_date': str(end_date)})

    return data, r.status_code


def get_properties(resource, headers={}):
    """ get JSON properties of a resource """
    my_headers = headers.copy()
    my_headers['Accept']="application/json"
    r = requests.get(resource, headers=my_headers, auth=api.get_credential(), verify=False)
    if r.status_code != 200:
        raise RuntimeError
    else:
        return r.json()


def get_working_directory(job_id, headers={}, properties=None):
    """ returns the URL of the working directory resource of a job """
    if properties is None:
        properties = get_properties(job_id, headers)
    return properties['_links']['workingDirectory']['href']


def invoke_action(job_url, action, headers, data={}):
    my_headers = headers.copy()
    my_headers['Content-Type']="application/json"
    properties = get_properties(job_url, headers)
    action_url = properties['_links']['action:' + action]['href']
    return requests.post(action_url, headers=my_headers, data=json.dumps(data), auth=api.get_credential(), verify=False)


def upload(destination, file_desc, headers):
    my_headers = headers.copy()
    my_headers['Content-Type'] = "application/octet-stream"
    name = file_desc['To']
    data = file_desc['Data']
    # TODO file_desc could refer to local file
    r = requests.put(destination + "/" + name, data=data, headers=my_headers, auth=api.get_credential(), verify=False)
    return r


def submit(job, headers, inputs=[]):
    """
    Submits a job to the given URL, which can be the ".../jobs" URL
    or a ".../sites/site_name/" URL
    If inputs is not empty, the listed input data files are
    uploaded to the job's working directory, and a "start" command is sent
    to the job.
    """
    data = {}
    my_headers = headers.copy()
    my_headers['Content-Type'] = "application/json"
    if len(inputs) > 0:
        # make sure UNICORE does not start the job
        # before we have uploaded data
        job['haveClientStageIn'] = 'true'

    r = requests.post(url=api.JOBS_URL, data=json.dumps(job), headers=my_headers, auth=api.get_credential(), verify=False)
        
    if r.status_code == 201:
        job_url = r.headers['Location']
        data['job_id'] = get_job_id(job_url)

        #  upload input data and explicitely start job
        if len(inputs) > 0:
            working_directory = get_working_directory(job_url, headers)
            # working_directory = api.get_working_directory_url(data['job_id'].lower())
            for i in inputs:
                upload(working_directory + "/files", i, headers)
        invoke_action(job_url, "start", headers)
       
        r = requests.get(url=job_url, auth=api.get_credential(), verify=False)
         
        if r.status_code == 200:
            json_job = r.json()
            data.update({
                'stage': json_job['status'],
                'init_date': json_job['submissionTime']
            })
    
    else:
        data = r.content
    
    return data, r.status_code


def abort_job(job_id, headers={}):
    """ Abort/Cancel a job. """
    my_headers = headers.copy()
    job_url = api.JOBS_URL + '/' + job_id.lower()
    r = invoke_action(job_url, 'abort', my_headers)
    if r.status_code == 200:
        match = re.findall('Job was aborted by the user', str(r.json()['log']))
        if len(match) > 1:
            data = 'Aborted'
            return data, r.status_code
    return r.content, r.status_code 
    

def get_job_files_list(job_id, headers={}):
    data = []
    job_id = job_id.lower()
    r = api.get_job_file_list(job_id=job_id.lower(), headers=headers)
    print r.status_code, r.content
    if r.status_code == 200:
        soup = BeautifulSoup(r.content)
        file_list = soup.findAll("ul")[0].findAll("li")

        for f in file_list:
            data.append(re.findall("/[a-zA-Z0-9-_.]+", str(f))[0])

    return data, r.status_code


def download_job_file(job_id, file_id=None, headers={}):
    r = api.download_job_file(job_id=job_id.lower(), file_id=file_id, headers=headers)
    return r.content, r.status_code


def advance_endpoint(method, url, headers, data=None, json=None):
    new_headers = headers.copy()
    URL = api.URL + url
    print 'Advaced Pizdaint request FINAL URL = ' + URL
    if method == 'GET':
        r = requests.get(url=URL, headers=new_headers, data=data, json=json, auth=api.get_credential(), verify=False)
    elif method == 'POST':
        r = requests.post(url=URL, headers=new_headers, data=data, json=json, auth=api.get_credential(), verify=False)
    elif method == 'PUT':
        r = requests.put(url=URL, headers=new_headers, data=data, json=json, auth=api.get_credential(), verify=False)
    elif method == 'DELETE':
        r = requests.delete(url=URL, headers=new_headers, data=data, json=json, auth=api.get_credential(), verify=False)

    return r
