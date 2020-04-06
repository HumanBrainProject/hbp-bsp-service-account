from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import avm.admin_views as views

urlpatterns = [

    # give all the jobs from all hpc from all projects for all users
    url(r'^admin/jobs/$', views.JobsView.as_view()),
    # give all jobs from specified hpc for all users
    url(r'^admin/jobs/(?P<hpc>[a-zA-Z-_]+)/$', views.JobsView.as_view()),
    # give all jobs from the specified hpc and project for all users
    url(r'^admin/jobs/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.JobsView.as_view()),
    # give all the jobs from the specified hpc project for single job
    url(r'^admin/jobs/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/(?P<job_id>[A-Z0-9-_]+)/$', views.JobsView.as_view()),

    url(r'^admin/jobs/(?P<user_id>[0-9]+)/$', views.UserJobsView.as_view()),
    # give all jobs from specified hpc for a single user
    url(r'^admin/jobs/(?P<user_id>[0-9]+)/(?P<hpc>[a-zA-Z-_]+)/$', views.UserJobsView.as_view()),
    # give all jobs from the specified hpc and project for a single user
    url(r'^admin/jobs/(?P<user_id>[0-9]+)/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.UserJobsView.as_view()),
    # give all the jobs from the specified hpc project for a single user
    url(r'^admin/jobs/(?P<user_id>[0-9]+)/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/(?P<job_id>[A-Z0-9-_]+)/$', views.UserJobsView.as_view()),

    # give all projects for all hpc
    url(r'^admin/projects/$', views.ProjectsView.as_view()),
    # give all projects from specified hpc
    url(r'^admin/projects/(?P<hpc>[a-zA-Z-_]+)/$', views.ProjectsView.as_view()),
    # give the single project for the hpc
    url(r'^admin/projects/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.ProjectsView.as_view()),

    # get all quotas for all projects for all hpc
    url(r'^admin/quotas/$', views.QuotaView.as_view()),
    # get all quotas for all projects for the specified hpc
    url(r'^admin/quotas/(?P<hpc>[a-zA-Z-_]+)/$', views.QuotaView.as_view()),
    # get all quotas for the specified project for the specified hpc
    url(r'^admin/quotas/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.QuotaView.as_view()),

    # get all quotas for a single user
    url(r'^admin/quotas/(?P<user_id>[0-9]+)/$', views.QuotaUserView.as_view()),
    # get all quotas for all projects for the specific hpc for a single user
    url(r'^admin/quotas/(?P<user_id>[0-9]+)/(?P<hpc>[a-zA-Z-_]+)/$', views.QuotaUserView.as_view()),
    # get all quota for the specific project for the specific hpc for a single user
    url(r'^admin/quotas/(?P<user_id>[0-9]+)/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.QuotaUserView.as_view()),

    # get all users
    url(r'^admin/users/$', views.UserView.as_view()),

    # add and remove users from groups(project)
    url(r'^admin/groups/add/(?P<user_id>[0-9]+)/(?P<project_id>[0-9]+)/$', views.UserGroupAdd.as_view()),
    url(r'^admin/groups/remove/(?P<user_id>[0-9]+)/(?P<project_id>[0-9]+)/$', views.UserGroupRemove.as_view()),

    # ban and unban users from project
    url(r'^admin/ban/(?P<user_id>[0-9]+)/(?P<project_id>[0-9]+)/$', views.UserBan.as_view()),
    url(r'^admin/unban/(?P<user_id>[0-9]+)/(?P<project_id>[0-9]+)/$', views.UserUnBan.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
