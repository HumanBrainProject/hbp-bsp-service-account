# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import status

from avm.utils.misc import get_user
from avm.models import Project

import requests


class IsAdmin(permissions.BasePermission):
    """
    This custom permission enable admins to access the "admin_views.py" apis.
    """
    message = 'User is not Administrator.'

    def has_permission(self, request, view):
        """ Return true if user is admin. """
        # if user is 'admin' get permission
        user = get_user(request)
        if user.is_admin:
            return True
        return False


import pprint
class IsInGroups(permissions.BasePermission):
    """
    This custom permission allow users to access api based on groups
    """
    message = 'User is not belong to this group.'

    def has_permission(self, request, view):
        """ Return true if user can access the api. """
        user = get_user(request)

        # get permission if you come from hhnb
        if request.META['REQUEST_URI'] == '/jobs/pizdaint/hhnb_daint_cscs/':
            r = requests.get('https://hbp-bsp-hhnb.cineca.it/hh-neuron-builder/status', stream=True)
            if r.status_code == 200:
                hhnb_ip, _ =  r.raw._connection.sock.getpeername()
                if request.META['REMOTE_ADDR'] == hhnb_ip:
                    return True
        
        if user:
            user_groups = user.groups.split(',')
            print(user_groups)
            if user_groups == '':
                return False
            group = request.path.split('/')[2:-1]
            if len(group) < 2:
                return True
            elif len(group) >= 2:
                try:
                    project = Project.objects.get(hpc=group[0].upper(), name=group[1])
                    if str(project.id) in user_groups:
                        return True
                except Project.DoesNotExist:
                    return Response('Project not found!', status=status.HTTP_404_NOT_FOUND)
        return False


class IsNotBanned(permissions.BasePermission):
    """
    This custom permission unable banned users to perform requests to the Service Account.
    """
    message = 'User is banned from this project.'

    def has_permission(self, request, view):
        """ Return false if user is banned. """
        user = get_user(request)
        if user.banned_from:
            return False
        return True
