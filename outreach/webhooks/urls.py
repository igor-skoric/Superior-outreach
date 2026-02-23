from django.urls import path
from .views import ingest_webhook

urlpatterns = [
    path("ingest/", ingest_webhook, name="webhook_ingest"),
]