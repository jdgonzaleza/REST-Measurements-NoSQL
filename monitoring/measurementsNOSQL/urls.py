from django.conf.urls import url, include

from .views import *

urlpatterns =[
    url(r'^variables/$', variables),
    url(r'^variables/(?P<pk>[0-9]+)$', variablesDetail),
    url(r'^lugares/$', lugar),
    url(r'^lugares/(?P<pk>[0-9]+)$', lugarDetail),
    url(r'^alertas/$', alerta),
    url(r'^alertas/(?P<pk>[0-9]+)$', alertaDetail)
]