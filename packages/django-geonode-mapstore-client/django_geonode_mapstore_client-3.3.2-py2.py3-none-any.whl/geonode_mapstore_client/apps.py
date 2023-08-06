# -*- coding: utf-8 -*-
#########################################################################
#
# Copyright 2015-2018, GeoSolutions Sas.
# All rights reserved.
#
# This source code is licensed under the BSD-style license found in the
# LICENSE file in the root directory of this source tree.
#
#########################################################################
from django.apps import AppConfig as BaseAppConfig
from django.utils.translation import ugettext_lazy as _
from django.apps import apps
from django.conf import settings as django_settings


def run_setup_hooks(*args, **kwargs):
    from geonode.urls import urlpatterns
    from django.conf.urls import url, include

    urlpatterns += [
        url(r'^mapstore/', include('mapstore2_adapter.urls')),
        url(r'^', include('mapstore2_adapter.geoapps.geostories.api.urls')),
        url(r'^', include('mapstore2_adapter.geoapps.dashboards.api.urls')),
    ]
    
    # adding default format for metadata schema validation
    django_settings.EXTRA_METADATA_SCHEMA = {
        **django_settings.EXTRA_METADATA_SCHEMA,
        **{
            "geostory": django_settings.DEFAULT_EXTRA_METADATA_SCHEMA,
            "dashboard": django_settings.DEFAULT_EXTRA_METADATA_SCHEMA 
        }
    }


class AppConfig(BaseAppConfig):

    name = "geonode_mapstore_client"
    label = "geonode_mapstore_client"

    def ready(self):
        if not apps.ready:
            run_setup_hooks()
        super(AppConfig, self).ready()
