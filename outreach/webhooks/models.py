from django.db import models


class WebhookEvent(models.Model):
    source = models.CharField(max_length=64, blank=True, default="")      # npr. "trellus", "stripe", "ringcentral"
    event_type = models.CharField(max_length=128, blank=True, default="") # npr. "call.created"
    external_id = models.CharField(max_length=128, blank=True, default="")# id iz payload-a ako postoji
    headers = models.JSONField(default=dict, blank=True)
    payload = models.JSONField()
    signature = models.CharField(max_length=512, blank=True, default="")
    received_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default="received")          # received/processed/failed

    class Meta:
        indexes = [
            models.Index(fields=["source", "event_type"]),
            models.Index(fields=["external_id"]),
            models.Index(fields=["received_at"]),
        ]