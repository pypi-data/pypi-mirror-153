from rest_framework import serializers

from contentful_webhook_receiver.models import WebhookInvocation


class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebhookInvocation
        fields = ['data', 'type']
