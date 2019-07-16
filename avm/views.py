# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import FileResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, FileUploadParser
from rest_framework.renderers import JSONRenderer

from serializers import *
from nsg import nsg
from pizdaint import pizdaint
from pizdaint.utils.params import check_payload as check_pizdaint_value
from utils.misc import get_user, get_nsg_enduser, update_job_status_and_quota, hpc_exists
from service_account.settings import DEFAULT_PROJECT as PROJECT, ENABLED_HPC as HPC
from permissions import IsInGroups, IsNotBanned

import logging
import json


logging.basicConfig()
logger = logging.getLogger(__name__)


class ServiceStatus(APIView):
    """
    This API is used to check if the Service Account is up.  
    """

    renderer_classes = (JSONRenderer, )

    def get(self, request):
        response = {'bsp-service-account-status': 1}
        return Response(response, status=status.HTTP_200_OK)


class HPCAvailable(APIView):
    """
    This API is used to get a list of the all HPC systems available on the Service Account.
    """
    
    renderer_classes = (JSONRenderer, )

    def get(self, request, hpc=None):
        if not hpc:
            return Response(json.dumps([h for h, _ in HPC]), status=status.HTTP_200_OK)
        elif hpc.upper() in [h for h, _ in HPC]:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)


class JobsView(APIView):
    """
    JobsView is used to submit job to HPC systems and also to retrieve
    all jobs or a specified job's info (e.g. status, submitting date, ecc...).

    Allowed methods are:
        GET:    to retrieve info about a previously submitted job from the local DB.
                If the specified job is not completed, the request is forwarded to the HPC system;
        POST:   to submit a job to an HPC system. Right now works only with the NSG Supercomputer;
        DELETE: to delete a job from an HPC system and from local Database;
    """

    parser_classes = (JSONParser, FileUploadParser,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsInGroups, IsNotBanned)

    def get(self, request, hpc=None, project_name=None, job_id=None):
        """
        The request queries for job or jobs object to the local database.
        If the request is send from an AdminUser, the response returns all jobs object.

        If all parameters are omitted, then the method returns all user's jobs.
        If only hpc_name is specified, then the method all user's jobs submitted on that HPC.
        If the project_name is specified, then the method returns all user's jobs submitted on that project of that HPC.
        If also the job_id is specified, then the method returns the single job with that id submitted on that project of that HPC.

        """
        logger.debug('JobsView--->GET: Called.')
        user = get_user(request)
        if not isinstance(user, User):
            logger.warning('JobsView--->GET: User not recognized.\n' +
                           ' ================= USER ERRORS ====================\n' + user +
                           ' ==================================================')
            return Response(user, status=status.HTTP_403_FORBIDDEN)
        # if hpc is set, check if it exists and then returns all user's job submitted on that HPC
        if hpc:
            hpc = hpc.upper()
            if hpc_exists(hpc):
                # if project_name is set returns all user's job submitted on that project of that HPC
                if project_name:
                    try:
                        project = Project.objects.get(name=project_name)
                        # if job_id is set returns the job instance with that job_id on that project on that HPC
                        if job_id:
                            try:
                                # update and return the single job
                                update_job_status_and_quota(user=user, project=project, job_id=job_id)
                                job = Job.objects.get(owner=user, project=project, job_id=job_id)
                                serializer = JobSerializer(job)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            except Job.DoesNotExist:
                                return Response('Job not found!', status=status.HTTP_404_NOT_FOUND)
                        # update and return all jobs for the specified project
                        update_job_status_and_quota(user=user, project=project)
                        jobs = Job.objects.filter(owner=user, project=project)
                        serializer = JobSerializer(jobs, many=True)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
                # update and return all jobs submitted into the specified hpc
                update_job_status_and_quota(user=user, hpc=hpc)
                projects = Project.objects.filter(hpc=hpc)
                jobs = Job.objects.filter(owner=user, project=projects)
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                # if hpc is wrong returns 404 error code
                return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)
        # update and return all user's jobs
        update_job_status_and_quota(user=user)
        jobs = Job.objects.filter(owner=user)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, hpc, project_name=None):
        """
        The POST method allow user to submit a job to the chosen HPC. If project name is not set, then the default
        one of the HPC is automatically selected.

        The filename must be set into headers as 'Content-Disposition: attachment; filename=some_filename'.

        If project is not found on the chosen HPC, a 400 error code is returned.

        Parameter fields must to be pass as header's payload
            'tool' indicates which tool user want to use to run job;
            'n_cores' indicates how many cores are used to run job;
            'n_nodes' indicates how many nodes want to use;
            'runtime' indicate how many cpu-hours are assigned to run job;

        :return: Response object with data of successes job submissions and 201 status code otherwise
                 data errors and 401 status code if user has not enough quota or error 400 if the request
                 is in a bad format.
        """
        # logger.debug('JobsView--->POST: Called.')

        user = get_user(request)

        # check if user is not anonymous
        if not isinstance(user, User):
            # logger.warning('JobsView--->POST: User not recognized.\n' +
            #               ' ================= USER ERRORS ====================\n' + user +
            #               ' ==================================================')
            return Response(user, status=status.HTTP_403_FORBIDDEN)

        hpc = hpc.upper()

        # if project is not set then submit on the default one of the specified hpc
        if not project_name:
            project_name = PROJECT[hpc]
        # else set the one user demands
        try:
            project = Project.objects.get(name=project_name, hpc=hpc)
        except Project.DoesNotExist:
            # logger.warning('JobsView--->POST: Project not found.')
            return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
        # logger.info('JobsView--->POST: Project set: ' + str(project) + '.')

        # checking for user quota
        try:
            quota = Quota.objects.get(user=user, project=project)
        except Quota.DoesNotExist:
            # logger.warning('JobsView--->POST: User ' + str(user) + ' not have quota.')
            return Response('User has not quota!', status=status.HTTP_401_UNAUTHORIZED)

        # =================== PAYLOAD FORM = {"key": "value"} - doesn't work with single quotes =======================
        # payload must to be extract from request.META because with fileUploading it's not possible to get request.data
        try:
            raw_payload = request.META['HTTP_PAYLOAD']
            payload = json.loads(raw_payload)
        except KeyError:
            # logger.info('JobsView--->POST: Payload not found!')
            return Response('Request incomplete. Parameters missing!', status=status.HTTP_400_BAD_REQUEST)

        # check for job file
        try:
            job_file = request.FILES['file']
        except KeyError:
            if hpc == 'NSG':
                # logger.info('JobsView--->POST: Input file not found!')
                return Response('Request incomplete. Input file missing!', status=status.HTTP_400_BAD_REQUEST)

        runtime = float(payload['runtime']) * 60 * 60
        # check if user has enough quota to run the job
        try:
            quota.sub(time=runtime)
        except ValueError:
            # check for jobs status of the selected project if user has not enough quota
            update_job_status_and_quota(user=user, project=project)
            # logger.info('Updating jobs for user ' + str(user) + '.')

            # if quota is still not enough return a 'Quota not enough' message to user
            try:
                quota.sub(time=runtime)
            except ValueError:
                # logger.warning('User ' + str(user) + ' hasn't enough quota on this project ' + str(project) + ' to run the job.')
                return Response(data='Quota not enough!', status=status.HTTP_401_UNAUTHORIZED)

        # check for job title parameters into payload
        try:
            job_title = payload['title']
        except KeyError:
            job_title = ''

        # submit on NSG
        if hpc == 'NSG':
            data, status_code = nsg.submit_job(enduser=get_nsg_enduser(user), payload=payload, infile=job_file)
            # restore job's runtime if submit goes wrong
            if status_code != 201 and status_code != 200:
                quota.add(runtime)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # submit on PIZDAINT
        elif hpc == 'PIZDAINT':
            inputs = []
            try:
                job_file_name = request.META['HTTP_CONTENT_DISPOSITION'].split('filename=')[1]
                job_input = {'To': job_file_name, 'Data': job_file.read()}
                inputs = [job_input]
            except KeyError:
                logger.info('No input file for pizdaint job')
            try:
                check_pizdaint_value(payload)
            except ValueError:
		return Response('Core number must be at least equal to 12 and node number at least equal to 1!', status=status.HTTP_400_BAD_REQUEST)
            pizdaint_job = {
                "Executable": payload['command'],
                "Resources": {
                    "Project": "ich011",
                    "Nodes": payload['node_number'],
                    "CPUsPerNode": payload['core_number'],
                    "Runtime": str(runtime / 60) + 'm',
                    "NodeConstraints": "mc",
                },
            }
            data, status_code = pizdaint.submit(job=pizdaint_job, headers={}, inputs=inputs)

            # restore job's runtime if submit goes wrong
            if status_code != 201 and status_code != 200:
                quota.add(time=runtime)
                return Response(data, status=status.HTTP_400_BAD_REQUEST)

        # update other job values
        data.update({
            'owner': user.id,
            'project': project.id,
            'title': job_title,
            'runtime': payload['runtime'],
            'end_date': None
        })

        # serializer and save the job if everything is ok
        serializer = JobSerializer(data=data)
        if serializer.is_valid():
            job = serializer.save()
            # logger.debug('JobsView--->POST: Job "' + str(job) + '" submitted.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hpc, project_name, job_id):
        """
        Delete or Cancel a job.
        Deleting a job means that the job was completed and user choose to delete it from the HPC or it can happen
        that the job goes in timeout on HPC system and it is deleted.
        Canceling a job means that the job is not completed yet and it will be canceled restoring all the user quota
        allocated to run the job, it can happen because the job was submitted by mistake.
        """

        logger.debug('JobsView--->DELETE: Called.')

        user = get_user(request)
        if not isinstance(user, User):
            logger.warning('JobsView--->DELETE: User not recognized.\n' +
                           ' ================= USER ERRORS ====================\n' + user +
                           ' ==================================================')
            return Response(user, status=status.HTTP_403_FORBIDDEN)

        hpc = hpc.upper()
        if not hpc_exists(hpc):
            return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)

        try:
            project = Project.objects.get(hpc=hpc, name=project_name)
            job = Job.objects.get(job_id=job_id, project=project)
            if job.stage == 'DELETED' or job.stage == 'CANCELED':
                return Response('Job is already deleted/canceled', status=status.HTTP_200_OK)
            if hpc == 'NSG':
                content, status_code = nsg.delete_job(enduser=get_nsg_enduser(user), jobid=job_id)
                if status_code == 204:
                    # update job
                    if job.terminal_stage:
                        # delete job if is completed
                        job.stage = 'DELETED'
                    else:
                        # cancel job if it is not completed yet and restore quota
                        job.stage = 'CANCELED'
                        quota = Quota.objects.get(user=user, project=job.project)
                        quota.add(time=job.runtime)
                else:
                    # if the delete request goes wrong returns the error and the status_code
                    return Response(content, status=status_code)
            elif hpc == 'PIZDAINT':
                content, status_code = pizdaint.abort_job(job_id=job_id)
                if status_code != 200:
                    # if the delete request goes wrong returns the error and the status_code
                    return Response(content, status=status_code)
                if content == 'Aborted':
                    # update job
                    if job_terminal_stage:
                        # deleted job if is completed
                        job.stage = 'DELETED'
                    else:
                        # cancel job if it is not completed yet and restore quota
                        job.stage = 'CANCELED'
                        quota = Quota.objects.get(user=user, project=job.project)
                        quota.add(time=job.runtime)
            job.save()
            serializer = JobSerializer(job)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
        except Job.DoesNotExist:
            return Response('Job not found!', status=status.HTTP_404_NOT_FOUND)


class FilesView(APIView):
    """
    FilesView is used to get files object (e.g. job's results) from HPC systems.

    Allowed methods are:
        GET:    retrieve the specified file (e.g the output/results of the a specific job) from the HPC system.
    """

    permission_classes = (IsInGroups, IsNotBanned)

    def get(self, request, hpc, project_name, job_id, fileid=None):
        """
        Perform the GET request to NSG-R to retrieve a specific job's files list or to download a file.

        :param request: the request object.
        :param jobid: jobid required to perform the request. Specify the job in which user wants to get the files.
        :param fileid: if fileid is set, the request return the specific file user wants to get.
        :return: return the file specified by fileid or the job's files list.
        """
        logger.debug('FilesView--->GET: called.')

        user = get_user(request)

        if not isinstance(user, User):
            logger.warning('FilesView--->GET: User not recognized.\n' +
                           ' ================= USER ERRORS ====================\n' + user +
                           ' ==================================================')
            return Response(user, status=status.HTTP_403_FORBIDDEN)
        hpc = hpc.upper()
        if hpc not in [i[0] for i in HPC]:
            return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)
        try:
            project = Project.objects.get(name=project_name)
            try:
                job = Job.objects.get(owner=user, project=project, job_id=job_id)
                if job.project.hpc == 'NSG':
                    # getting files list from NSG
                    if not fileid:
                        if job.terminal_stage:
                            files, status_code = nsg.get_job_files_list(enduser=get_nsg_enduser(user), jobid=job_id)
                        else:
                            files, status_code = nsg.list_workingdir_files(enduser=get_nsg_enduser(user), jobid=job_id)
                        return Response(files, status=status_code)
                        # getting file object from NSG
                    else:
                        if job.terminal_stage:
                            outfile, status_code = nsg.download_output_file(enduser=get_nsg_enduser(user), jobid=job_id, fileid=fileid)
                        else:
                            outfile, status_code = nsg.download_working_directory_file(enduser=get_nsg_enduser(user), jobid=job_id, filename=fileid)
                        return FileResponse(outfile, status=status_code)

                elif job.project.hpc == 'PIZDAINT':
                        # getting files list from PIZDAINT
                    if not fileid:
                        file_list, status_code = pizdaint.get_job_files_list(job_id=job_id)
                        return Response(data=file_list, status=status_code)
                    else:
                        outfile, status_code = pizdaint.download_job_file(job_id=job_id, file_id=fileid)
                        return FileResponse(outfile, status=status_code)

            except Job.DoesNotExist:
                return Response('Job not found!', status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)


class ProjectsView(APIView):
    """
    ProjectsView is used to create, retrieve and delete projects.
    A project is intended as a virtual space into users can run jobs.

    Allowed methods are:
        GET:    retrieve a specified project.
        POST:   create a new project.
        DELETE: delete a specified project.
    """

    render_classes = (JSONRenderer, )

    def get(self, request, hpc=None, project_name=None):

        logger.debug('ProjectsView--->GET: called.')

        if hpc:
            hpc = hpc.upper()
            if hpc not in [i[0] for i in HPC]:
                return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)
            if project_name:
                try:
                    project = Project.objects.get(name=project_name, hpc=hpc)
                    serializer = ProjectSerializer(project)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Project.DoesNotExsist:
                    return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
            try:
                projects = Project.objects.filter(hpc=hpc)
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Project.DoesNotExist:
                return Response('Projects not found!', status=status.HTTP_404_NOT_FOUND)

        try:
            projects = Project.objects.all()
            serializer = ProjectSerializer(projects, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response('No projects', status=status.HTTP_204_NO_CONTENT)


class QuotasView(APIView):
    """
    QuotasView is used to create. retrieve, update and delete information about the user quotas.
    The quota object is composed by the cpu time (in seconds), disk space (in kilobyte), user and project.
    If the user has no enough time or space for that project, he can't submit other job.

    Allowed methods are:
        GET:    retrieve a specified quota record.
        POST:   create a new quota record.
        DELETE: delete a quota record.
    """

    renderer_classes = (JSONRenderer,)

    def get(self, request, hpc=None, project_name=None):

        logger.debug('QuotasView--->GET: called.')

        user = get_user(request)

        if hpc:
            hpc = hpc.upper()
            if hpc not in [i[0] for i in HPC]:
                return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)

            if project_name:
                try:
                    project = Project.objects.get(name=project_name, hpc=hpc)
                    try:
                        quota = Quota.objects.get(user=user, project=project)
                        serializer = QuotaSerializer(quota)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except Quota.DoesNotExist:
                        return Response('Quota not found!', status=status.HTTP_404_NOT_FOUND)
                except Project.DoesNotExist:
                    return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
            else:
                projects = Project.objects.filter(hpc=hpc)
                quotas = Quota.objects.filter(project=projects, user=user)
                serializer = QuotaSerializer(quotas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        quotas = Quota.objects.filter(user=user)
        serializer = QuotaSerializer(quotas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
