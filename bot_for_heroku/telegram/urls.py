from django.urls import include,path
from telegram.views import UpdateBot
from django.conf.urls import url

urlpatterns = [
    url(r'^$', UpdateBot.as_view(),name='hook'),
]
