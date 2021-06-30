from django.urls import include,path
from telegram.views import UpdateBot

urlpatterns = [
    path('', UpdateBot.as_view(),name='hook'),
]
