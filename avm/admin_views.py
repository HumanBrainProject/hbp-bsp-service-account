# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from avm.serializers import *
from avm.utils.misc import hpc_exists
from avm.permissions import IsAdmin
from service_account.settings import ENABLED_HPC as HPC


class JobsView(APIView):
    """
    This class allow admins to query for jobs filtered by HPC, project or directly query for a specific job
    specifying the HPC, the project and the relative job_id.
    """

    parser_classes = (JSONParser, )
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, hpc=None, project_name=None, job_id=None):

        if hpc:
            hpc = hpc.upper()
            if hpc in [i[0] for i in HPC]:

                if project_name:
                    try:
                        project = Project.objects.get(name=project_name, hpc=hpc)
                        if job_id:
                            try:
                                job = Job.objects.get(job_id=job_id, project=project)
                                serializer = JobSerializer(job)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            except Job.DoesNotExist:
                                return Response('Job not found!', status=status.HTTP_404_NOT_FOUND)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)

                projects = Project.objects.filter(hpc=hpc)
                jobs = Job.objects.filter(project=projects)
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserJobsView(APIView):
    """
    This class allow admins to query for jobs of a specific user. The admin can also filters the query specifying
    the HPC, the project and the job_id.
    """

    parser_classes = (JSONParser, )
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, user_id, hpc=None, project_name=None, job_id=None):

        if hpc:
            hpc = hpc.upper()
            if hpc in [i[0] for i in HPC]:

                if project_name:
                    try:
                        project = Project.objects.get(name=project_name, hpc=hpc)
                        if job_id:
                            try:
                                job = Job.objects.get(job_id=job_id, project=project, owner=user_id)
                                serializer = JobSerializer(job)
                                return Response(serializer.data, status=status.HTTP_200_OK)
                            except Job.DoesNotExist:
                                return Response('Job not found!', status=status.HTTP_404_NOT_FOUND)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)

                projects = Project.objects.filter(hpc=hpc)
                jobs = Job.objects.filter(project=projects, owner=user_id)
                serializer = JobSerializer(jobs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

        jobs = Job.objects.filter(owner=user_id)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProjectsView(APIView):

    parser_classes = (JSONParser,)
    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAdmin, )

    def get(self, request, hpc=None, project_name=None):
        if hpc:
            if hpc_exists(hpc):
                hpc = hpc.upper()
                if project_name:
                    try:
                        print(hpc, project_name)
                        project = Project.objects.get(hpc=hpc, name=project_name)
                        serializer = ProjectSerializer(project)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
                projects = Project.objects.filter(hpc=hpc)
                serializer = ProjectSerializer(projects, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response('HPC not exists!', status=status.HTTP_400_BAD_REQUEST)
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProjectSerializer(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, hpc, project_name):
        hpc = hpc.upper()
        if hpc_exists(hpc):
            try:
                project = Project.objects.get(hpc=hpc, name=project_name)
                project.delete()
                return Response('Project deleted!', status=status.HTTP_204_NO_CONTENT)
            except Project.DoesNotExist:
                return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
        else:
            return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)


class QuotaView(APIView):

    parser_classes = (JSONParser, )
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, hpc=None, project_name=None):

	
        if hpc and hpc_exists(hpc):
            hpc = hpc.upper()

            if project_name:
                try:
                    project = Project.objects.get(hpc=hpc, name=project_name)
                    quotas = Quota.objects.filter(project=project)
                    serializer = QuotaSerializer(quotas, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
                except Quota.DoesNotExist:
                    return Response('Quota not found!', status=status.HTTP_404_NOT_FOUND)

            try:
                projects = Project.objects.filter(hpc=hpc)
                quotas = Quota.objects.filter(project=projects)
                serializer = QuotaSerializer(quotas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Project.DoesNotFound:
                return Response('No quotas found!', status=status.HTTP_404_NOT_FOUND)

        try:
            quotas = Quota.objects.all()
            serializer = QuotaSerializer(quotas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quota.DoesNotExist:
            return Response('No quotas found!', status=status.HTTP_404_NOT_FOUND)

    def post(self, request, hpc, project_name):

        if hpc_exists(hpc):
            hpc = hpc.upper()

            if project_name:
                try:
                    project = Project.objects.get(hpc=hpc, name=project_name)
                    quota = Quota(project=project, user=request.data['user'])
                    serializer = QuotaSerializer(instance=quota)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_201_CREATED)
                    return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
                except Project.DoesNotExist:
                    return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)

        return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)

    def put(self, request, hpc, project_name):

        if hpc_exists(hpc):
            hpc = hpc.upper()

            if project_name:
                try:
                    project = Project.objects.get(hpc=hpc, name=project_name)
                    quota = Quota(project=project, user=request.data['user'])
                    serializer = QuotaSerializer(instance=quota, data=request.data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except Project.DoesNotExist:
                    return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)

        return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)


class QuotaUserView(APIView):

    parser_classes = (JSONParser, )
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, user_id, hpc=None, project_name=None):

        if hpc:
            hpc = hpc.upper()
            if hpc_exists(hpc):
 
                if project_name:
                    try:
                        project = Project.objects.get(hpc=hpc, name=project_name)
                        quota = Quota.objects.get(user=user_id, project=project)
                        serializer = QuotaSerializer(quota)
                        return Response(serializer.data, status=status.HTTP_200_OK)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
                    except Quota.DoesNotExist:
                        return Response('Quota not found!', status=status.HTTP_404_NOT_FOUND)

                projects = Project.objects.filter(hpc=hpc)
                quotas = Quota.objects.filter(project=projects, user=user_id)
                serializer = QuotaSerializer(quotas, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)

        else:
            quotas = Quota.objects.filter(user=user_id)
            serializer = QuotaSerializer(quotas, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, user_id, hpc=None, project_name=None):

        if hpc:
            hpc = hpc.upper()
            if hpc_exists(hpc):

                if project_name:
                    try:
                        project = Project.objects.get(hpc=hpc, name=project_name)
                        quota = Quota.objects.get(user=user_id, project=project)
                        quota.delete()
                        return Response('Quota deleted', status=status.HTTP_204_NO_CONTENT)
                    except Project.DoesNotExist:
                        return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
                    except Quota.DoesNotExist:
                        return Response('Quota not found!', status=status.HTTP_404_NOT_FOUND)

                projects = Project.objects.filter(hpc=hpc)
                quotas = Quota.objects.filter(user=user_id, project=projects)
                quotas.delete()
                return Response('Quotas deleted', status=status.HTTP_204_NO_CONTENT)

            return Response('HPC not found!', status=status.HTTP_404_NOT_FOUND)

        quota = Quota.objects.filter(user=user_id)
        quota.delete()
        return Response('Quotas deleted!', status=status.HTTP_204_NO_CONTENT)


class UserView(APIView):

    parser_classes = (JSONParser, )
    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserGroupAdd(APIView):

    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, user_id, project_id):
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
            user.add_group(project.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('User does not exist!', status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response('Project does not exist!', status=status.HTTP_404_NOT_FOUND)


class UserGroupRemove(APIView):

    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAdmin,)

    def get(self, request, user_id, project_id):
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
            try:
                user.remove_group(project.id)
            except ValueError:
                return Response('User does not belong to the group!', status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('User does not exist!', status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response('Project does not exist!', status=status.HTTP_404_NOT_FOUND)


class UserBan(APIView):

    renderer_classes = (JSONRenderer, )
    permission_classes = (IsAdmin, )

    def get(self, request, user_id, project_id):
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
            user.ban(project.id)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('User does not exist!', status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response('Project does not exist!', status=status.HTTP_404_NOT_FOUND)


class UserUnBan(APIView):

    renderer_classes = (JSONRenderer,)
    permission_classes = (IsAdmin,)

    def get(self, request, user_id, project_id):
        try:
            user = User.objects.get(id=user_id)
            project = Project.objects.get(id=project_id)
            try:
                user.unban(project.id)
            except ValueError:
                return Response('User is not ban yet from this project!', status=status.HTTP_400_BAD_REQUEST)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response('User does not exist!', status=status.HTTP_404_NOT_FOUND)
        except Project.DoesNotExist:
            return Response('Project does not exist!', status=status.HTTP_404_NOT_FOUND)
