from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import advanced_views as views

urlpatterns = [

    # advanced end point for pizdaint system
    url(r'^advanced/pizdaint/$', views.pizdaint),
    url(r'^advanced/pizdaint/(?P<project_name>[a-z0-9]+)/$', views.pizdaint)
        
]

urlpatterns = format_suffix_patterns(urlpatterns)
