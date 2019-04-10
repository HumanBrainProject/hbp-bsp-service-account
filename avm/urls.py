from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from avm import views


urlpatterns = [

    # Check if the the service is up
    url(r'^status/$', views.ServiceStatus.as_view()),    


    # GET all jobs of all projects (dates/max number)
    # POST explicitly the project and hpc together with the job
    # DELETE delete or cancel a specific job

    # gives all the jobs from all hpc from all projects for the user
    url(r'^jobs/$', views.JobsView.as_view()),

    # gives all jobs from specified hpc for a single user
    # submit job into the default project of the specified hpc
    # delete all jobs submitted into the single hpc
    url(r'^jobs/(?P<hpc>[a-zA-Z-_]+)/$', views.JobsView.as_view()),

    # gives all the jobs from the specified hpc and project
    # submit job into hpc's project
    # delete all jobs into the hpc's project
    url(r'^jobs/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.JobsView.as_view()),

    # gives all the jobs from the specified hpc and project for single job
    # delete the specific job
    url(r'^jobs/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/(?P<job_id>[A-Z0-9-_]+)/$', views.JobsView.as_view()),


    # Projects
    # GET all projects
    # GET all projects per HPC
    url(r'^projects/$', views.ProjectsView.as_view()), # get all projects
    url(r'^projects/(?P<hpc>[a-zA-Z-_]+)/$', views.ProjectsView.as_view()), # get all projects for a specified hpc


    # Quotas
    # get all quotas for all projects for all hpc per user
    url(r'^quotas/$', views.QuotasView.as_view()),
    # get all quotas for all projects for the specified hpc
    url(r'^quotas/(?P<hpc>[a-zA-Z-_]+)/$', views.QuotasView.as_view()),
    # get all quotas for the specified project for the specified
    url(r'^quotas/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/$', views.QuotasView.as_view()),


    # Files
    url(r'^files/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/(?P<job_id>[A-Z0-9-_]+)/$', views.FilesView.as_view()), # get all files per job
    url(r'^files/(?P<hpc>[a-zA-Z-_]+)/(?P<project_name>[a-z0-9-_]+)/(?P<job_id>[A-Z0-9-_]+)/(?P<fileid>[^/]+)/$', views.FilesView.as_view()), # get a specific file per job

]

urlpatterns = format_suffix_patterns(urlpatterns)
