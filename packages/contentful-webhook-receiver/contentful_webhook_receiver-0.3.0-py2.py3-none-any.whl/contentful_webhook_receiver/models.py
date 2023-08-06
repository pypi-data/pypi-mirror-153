# -*- coding: utf-8 -*-

import uuid

from django.db import models


class WebhookInvocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data = models.JSONField()
    type = models.CharField(max_length=255)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.created_at:%Y-%m-%d} | {self.type}'
