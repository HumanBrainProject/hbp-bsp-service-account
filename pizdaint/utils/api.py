from requests.auth import HTTPBasicAuth

from service_account.settings import PIZDAINT_USER as USER
from service_account.settings import PIZDAINT_PASSWORD as PASSWORD

import requests


ROOT_URL = 'https://brissago.cscs.ch:8080/DAINT-CSCS'
# URL = 'https://brissago.cscs.ch:8080/DAINT-CSCS/rest/core'
#ROOT_URL = 'https://unicoregw.cscs.ch:8080/DAINT-CSCS'
URL = ROOT_URL + '/rest/core'
JOBS_URL = URL + '/jobs'
SITES_URL = URL + '/sites'
REGISTRIES_URL = URL + '/registries'
STORAGES_URL = URL + '/storages'
TRANSFERS_URL = URL + '/transfers'
FACTORIES_URL = URL + '/factories'
STORAGEFACTORIES_URL = URL + '/storagefactories'


def get_credential(user=None, password=None):
    if user and password:
        return HTTPBasicAuth(user, password)
    return HTTPBasicAuth(USER, PASSWORD)


def get_all_jobs(user_token=None):
    print('[PIZDAINT]: get_all_jobs(user_token=%s) called.' % user_token)
    if user_token:
        return requests.get(url=JOBS_URL, headers=user_token, verify=False)
    return requests.get(url=JOBS_URL, auth=get_credential(), verify=False)


def get_job_status(job_id, headers={}, user_token=None):
    print('[PIZDAINT]: get_job_status(job_id=%s, headers=%s, user_token=%s) called.' % (job_id, headers, user_token))
    headers['Accept'] = 'application/json'
    if user_token:
        headers['Authorization'] = user_token
    job_url = JOBS_URL + '/' + job_id
    return requests.get(url=job_url, headers=headers, auth=get_credential(), verify=False)


def get_job_file_list(job_id, headers={}):
    file_list_url = STORAGES_URL + '/' + job_id + '-uspace/files'
    return requests.get(url=file_list_url, headers=headers, auth=get_credential(), verify=False)


def get_job_file_info(job_id, file_id, headers={}):
    headers['Accept'] = 'application/json'
    file_url = STORAGES_URL + '/' + job_id + '-uspace/files/' + file_id
    return requests.get(url=file_url, headers=headers, auth=get_credential(), verify=False)


def download_job_file(job_id, file_id, headers={}):
    file_url = STORAGES_URL + '/' + job_id + '-uspace/files/' + file_id
    headers['Accept'] = 'application/octet-stream'
    return requests.get(url=file_url, headers=headers, auth=get_credential(), verify=False)


def get_working_directory_url(job_id):
   return STORAGES_URL + '/' + job_id + '-uspace'  
