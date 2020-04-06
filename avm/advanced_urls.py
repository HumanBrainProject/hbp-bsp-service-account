from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

import avm.advanced_views as views

urlpatterns = [

    # advanced end point for unicore system
    url(r'advanced/pizdaint/rest/core/*', views.unicore_pizdaint),
]

urlpatterns = format_suffix_patterns(urlpatterns)
