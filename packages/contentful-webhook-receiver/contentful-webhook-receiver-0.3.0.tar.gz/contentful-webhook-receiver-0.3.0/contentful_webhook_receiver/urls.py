# -*- coding: utf-8 -*-
from django.urls import path

from contentful_webhook_receiver.views import WebHookReceiverView

app_name = 'contentful_webhook_receiver'

urlpatterns = [
    path('contentful-webhook/', WebHookReceiverView.as_view()),
]
