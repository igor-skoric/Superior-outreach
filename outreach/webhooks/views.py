import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import WebhookEvent

@csrf_exempt
@require_POST
def ingest_webhook(request):
    # 1) Uhvati raw body
    raw_body = request.body
    if not raw_body:
        return HttpResponseBadRequest("Empty body")

    # 2) Parse JSON
    try:
        data = json.loads(raw_body.decode("utf-8"))
    except Exception:
        return HttpResponseBadRequest("Invalid JSON")

    # 3) Snimi sve (headers + payload)
    headers = {k: v for k, v in request.headers.items()}
    signature = request.headers.get("X-Signature", "")  # promeni na header koji tvoj provider koristi

    event = WebhookEvent.objects.create(
        source=headers.get("X-Webhook-Source", ""),      # ili hardcode "trellus"
        event_type=data.get("type", "") if isinstance(data, dict) else "",
        external_id=(data.get("id", "") if isinstance(data, dict) else ""),
        headers=headers,
        payload=data,
        signature=signature,
    )

    return JsonResponse({"ok": True, "id": event.id})