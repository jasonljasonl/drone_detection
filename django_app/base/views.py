from django.db import models
from django.http import JsonResponse
from .tasks import kafka_producer_task, calcul_distance_task

def start_services(request):
    port = request.GET.get('port', '14551')
    kafka_producer_task.delay(port=port)
    calcul_distance_task.delay()
    return JsonResponse({'status':'services started...'})