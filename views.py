from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Event
import json

def calendar_events(request):
    """
    Fetch all events to display in the calendar.
    """
    events = Event.objects.all()
    data = [
        {
            'id': event.id,
            'title': event.title,
            'start': event.start.isoformat(),
            'end': event.end.isoformat() if event.end else None,
        }
        for event in events
    ]
    return JsonResponse(data, safe=False)

@csrf_exempt
def create_event(request):
    """
    Create a new event from the calendar.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        event = Event.objects.create(
            title=data.get('title'),
            start=data.get('start'),
            end=data.get('end'),
        )
        return JsonResponse({'id': event.id}, status=201)

@csrf_exempt
def update_event(request, event_id):
    """
    Update an event when it's moved on the calendar.
    """
    if request.method == 'PUT':
        data = json.loads(request.body)
        try:
            event = Event.objects.get(id=event_id)
            event.start = data.get('start')
            event.end = data.get('end')
            event.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'error': 'Event not found'}, status=404)
