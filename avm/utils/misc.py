from hbp_app_python_auth.auth import get_auth_header
from ctools import manage_auth

from service_account.settings import DEFAULT_PROJECT, HBP_MY_USER_URL, DUMP_JOB_PATH

from avm.models import *
from avm.serializers import UserSerializer, JobSerializer

from nsg import nsg
from pizdaint import pizdaint

import requests
import json
import logging
import os


logging.basicConfig()
logger = logging.getLogger(__name__)


def add_default_quota_for_user(user):
    keys = DEFAULT_PROJECT.keys()
    for i in keys:
        project = Project.objects.get(hpc=i, name=DEFAULT_PROJECT[i])
        quota = Quota(user=user, project=project)
        quota.save()


def get_user(request):
    """
    Is used to identify user from HBP token. If user doesn't exist into Database, a new one is created.
    """
    user_url = HBP_MY_USER_URL

    # Retrieving HBP user's token
    headers = {'Authorization': request.META['HTTP_AUTHORIZATION']}

    # Getting user's info from HBP_COLLAB
    r = requests.get(url=user_url, headers=headers)

    if r.status_code != 200:
        logger.debug("get_user(): User's HBP Token not valid... Try to renew it.")
        manage_auth.Token.renewToken(request)
        headers = {'Authorization': get_auth_header(request.user.social_auth.get())}
        r = request.get(url=user_url, headers=headers)

    j = json.loads(r.content)

    # Try to get user from Database. If user not exists it is created.
    try:

        logger.debug('get_user(): Getting user with id: ' + j['id'])
        user = User.objects.get(id=j['id'])

    except User.DoesNotExist:

        logger.debug('get_user(): User ' + j['username'] + ' and id: ' + j['id'] +
                     ' does not exist and it will be create.')

        emails = j['emails']
        institutions = j['institutions']
        institution = ''

        for e in emails:
            if e['primary']:
                email = e['value']
        for i in institutions:
            if i['primary']:
                institution = i['name']

        # If user has not set institution, it will be set automatically to 'UNKNOWN' and country to 'IT', otherwise
        # the country code is set as the email domain (uppercase) if it is not equal to 'com'
        if not institution:
            country = 'IT'
        elif email.split('.')[-1] != 'com':
            country = email.split('.')[-1].upper()
        else:
            logger.error('get_user(): Set country code for user ' + j['id'] + '.')

        data = {
            'id': j['id'],
            'username': j['username'],
            'email': email,
            'institution': institution,
            'country': country
        }
        
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            # if is all right user is saved and it's added to default projects
            user = serializer.save()
            logger.debug('get_user(): User ' + str(user) + ' was created successfully')
            add_default_quota_for_user(user)
        else:
            logger.debug('get_user(): Errors in user creation.\nget_user(): ========= ERROR: =========\nget_user():')  
            print serializer.errors
            return serializer.errors

    return user


def get_nsg_enduser(user):
    """
    Get the real end user information required by the NSG Umbrella-User.
    """
    return {
        'id': user.id,
        'eu': user.username,
        'email': user.email,
        'institution': user.institution,
        'country': user.country
    }


def update_job_status_and_quota(user, hpc=None, project=None, job_id=None):
    data = {}
    # if hpc is specified select all projects of that hpc and all jobs of these projects
    if hpc:
        projects = Project.objects.filter(hpc=hpc)
        jobs = Job.objects.filter(owner=user, project=projects)
    # if project is specified select all jobs for that project
    elif project and not job_id:
        jobs = Job.objects.filter(owner=user, project=project)
    # if job_id and project is specified get and update the single job
    elif project and job_id:
        jobs = Job.objects.filter(owner=user, project=project, job_id=job_id)
    # otherwise select all jobs
    else:
        jobs = Job.objects.filter(owner=user)
    for job in jobs:
        # get job 'job' from the database
        if not job.terminal_stage:
            if job.project.hpc == 'NSG':
                data, status_code = nsg.get_job_status(enduser=get_nsg_enduser(user), jobid=job.job_id)
            elif job.project.hpc == 'PIZDAINT':
                data, status_code = pizdaint.get_job_status(job=job)
                
            # updating job info if the request code is OK
            if status_code == 200:
                serializer = JobSerializer(instance=job, data=data, partial=True)
                if serializer.is_valid():
                    job = serializer.save()
                    # restore unused quota
                    if job.end_date:
                        delta_time = job.end_date - job.init_date
                        delta_seconds = delta_time.days * 24 * 60 * 60 + delta_time.seconds
                        logger.info('JobsView--->POST: restoring ' + str(delta_seconds) +
                                    ' quota time for user "' + str(user) + '".')
                        quota = Quota.objects.get(user=user, project=job.project)
                        quota.add(time=delta_seconds)
            # if the response requests got a 404 not found error, update job stage to DELETED
            elif status_code == 404:
                job.stage = 'DELETED'
                job.save()


def hpc_exists(hpc):
    hpc = hpc.upper()
    if hpc in [i[0] for i in HPC]:
        return True
    return False


def dump_job(user_id, hpc_name, job_id, job_description, job_file_name, job_file_content):
    os.chdir(DUMP_JOB_PATH)
    if not os.path.exists(user_id):
        os.mkdir(user_id)
    os.chdir(user_id)

    if not os.path.exists(hpc_name):
        os.mkdir(hpc_name)
    os.chdir(hpc_name)
    if not os.path.exists(str(job_id)):
        os.mkdir(str(job_id))
    os.chdir(str(job_id))
    if job_file_name and job_file_content:
        with open(job_file_name, 'wb') as fd:
            fd.write(job_file_content)
    with open('job_description.txt', 'w') as fd:
        fd.write(job_description)

    print '====== JOB DUMP ======'
    print 'UserId: ' + str(user_id) + ' JobId: ' + str(job_id)
    return
    
